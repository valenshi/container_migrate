package plugins

import (
	"context"
	"sample-scheduler-framework/pkg/apis"

	v1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/klog"
	framework "k8s.io/kubernetes/pkg/scheduler/framework/v1alpha1"
)

// plugin name
const Name = "sample-plugin"

type Args struct {
	FavoriteColor  string `json:"favorite_color,omitempty"`
	FavoriteNumber int    `json:"favorite_number,omitempty"`
	ThanksTo       string `json:"thanks_to,omitempty"`
}

type Sample struct {
	args   *Args
	handle framework.FrameworkHandle
}

func (s *Sample) Name() string {
	return Name
}

var _ framework.ScorePlugin = &Sample{}

func New(configuration *runtime.Unknown, f framework.FrameworkHandle) (framework.Plugin, error) {
	args := &Args{}
	if err := framework.DecodeInto(configuration, args); err != nil {
		return nil, err
	}
	klog.V(3).Infof("get plugin config args: %+v", args)
	return &Sample{
		args:   args,
		handle: f,
	}, nil
}

func (s *Sample) Score(ctx context.Context, state *framework.CycleState, p *v1.Pod, nodeName string) (int64, *framework.Status) {
	klog.V(3).Infof("enter Score()!!!")
	// node, err := s.handle.SnapshotSharedLister().NodeInfos().Get(nodeName)
	// if err != nil {
	// 	// 节点没有准备好
	// 	klog.Errorf("Node %q not found in cycle state: %v", nodeName, err)
	// 	return 0, framework.NewStatus(framework.Error, fmt.Sprintf("Node not found in cycle state: %v", nodeName))
	// }
	// klog.V(3).Infof("node: %v", node)
	hostinfo, err := apis.InitHostInfo(nodeName)
	klog.V(3).Infof("hostInfo: %v", hostinfo)
	if err != nil {
		klog.Error(err)
	}

	// 计算ECM指标的得分
	// v1 := hostinfo.Power_limit - hostinfo.Power
	ecmScore := 100 - (hostinfo.Power/hostinfo.Power_limit*20 + hostinfo.Energy_cost*16)
	klog.V(3).Infof(nodeName+"'s socre: %v", ecmScore)
	klog.V(3).Infof("exit Score()!!!")
	return int64(ecmScore), framework.NewStatus(framework.Success, "")
}

func (s *Sample) ScoreExtensions() framework.ScoreExtensions {
	return nil
}
