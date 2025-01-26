package conductor

import (
	"context"
	"time"

	"github.com/ethereum/go-ethereum/log"

	"github.com/ethereum-optimism/optimism/op-node/rollup"
	"github.com/ethereum-optimism/optimism/op-node/rollup/event"
	"github.com/ethereum-optimism/optimism/op-service/eth"
)

// SequencerActionEvent triggers the sequencer to start/seal a block, if active and ready to act.
// This event is used to prioritize sequencer work over derivation work,
// by emitting it before e.g. a derivation-pipeline step.
// A future sequencer in an async world may manage its own execution.
type CommitPayloadEvent struct {
	// if payload should be promoted to safe (must also be pending safe, see DerivedFrom)
	IsLastInSpan bool
	// payload is promoted to pending-safe if non-zero
	DerivedFrom eth.L1BlockRef

	Info eth.PayloadInfo
	Ref  eth.L2BlockRef
}

func (ev CommitPayloadEvent) String() string {
	return "commit-payload"
}

type BuildingState struct {
	Onto eth.L2BlockRef
	Info eth.PayloadInfo

	Started time.Time

	// Set once known
	Ref eth.L2BlockRef
}

type ExecEngine interface {
	GetPayload(ctx context.Context, payloadInfo eth.PayloadInfo) (*eth.ExecutionPayloadEnvelope, error)
}

type AsyncGossiper interface {
	Gossip(payload *eth.ExecutionPayloadEnvelope)
	Get() *eth.ExecutionPayloadEnvelope
	Clear()
	Stop()
	Start()
}

type SequencerClient interface {
	CommitUnsafePayload(*eth.ExecutionPayloadEnvelope) error
}

type ConductorHelper struct {
	ctx context.Context

	engine ExecEngine // Underlying execution engine RPC

	log         log.Logger
	rollupCfg   *rollup.Config
	spec        *rollup.ChainSpec
	sequencer   SequencerClient
	asyncGossip AsyncGossiper

	emitter event.Emitter
}

func NewConductorHelper(driverCtx context.Context, engine ExecEngine, log log.Logger, rollupCfg *rollup.Config,
	sequencer SequencerClient,
	asyncGossip AsyncGossiper,
) *ConductorHelper {
	return &ConductorHelper{
		ctx:         driverCtx,
		engine:      engine,
		log:         log,
		rollupCfg:   rollupCfg,
		spec:        rollup.NewChainSpec(rollupCfg),
		sequencer:   sequencer,
		asyncGossip: asyncGossip,
	}
}

func (d *ConductorHelper) AttachEmitter(em event.Emitter) {
	d.emitter = em
}

func (d *ConductorHelper) OnEvent(ev event.Event) bool {

	switch x := ev.(type) {
	case CommitPayloadEvent:
		d.onCommitPayload(x)

	default:
		return false
	}
	return true
}

func (d *ConductorHelper) onCommitPayload(ev CommitPayloadEvent) {
	const getPayloadTimeout = time.Second * 100
	ctx, cancel := context.WithTimeout(d.ctx, getPayloadTimeout)
	defer cancel()

	envelope, err := d.engine.GetPayload(ctx, ev.Info)

	if err != nil {
		if x, ok := err.(eth.InputError); ok && x.Code == eth.UnknownPayload { //nolint:all
			d.log.Warn("Cannot seal block, payload ID is unknown",
				"payloadID", ev.Info.ID, "payload_time", ev.Info.Timestamp)
		}
		return
	}
	d.asyncGossip.Gossip(envelope)
	d.sequencer.CommitUnsafePayload(envelope)
}
