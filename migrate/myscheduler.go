package myScheduler // 示例包名

import (
    "context"
    "fmt"

    "k8s.io/api/core/v1"
    "k8s.io/apimachinery/pkg/util/sets"
    "k8s.io/apimachinery/pkg/util/wait"
    schedulerapi "k8s.io/kubernetes/pkg/scheduler/api"
)

const mySchedulerName = "MyScheduler" // 调度器的名称

// MyScheduler 是实现调度器接口的一个结构体
type MyScheduler struct {
    // 在这里定义您的结构体成员
}

// Name 方法返回调度器的名称
func (s *MyScheduler) Name() string {
    return mySchedulerName
}

// Schedule 方法实现实际的调度逻辑
func (s *MyScheduler) Schedule(ctx context.Context, state *schedulerapi.StateData, pod *v1.Pod, nodeName string) (string, error) {

    // 预选阶段（FirstFit）
    candidates, err := s.findCandidateNodes(state, pod)
    if err != nil {
        return "", err
    }

    // 优选阶段（Priority）
    candidateScores := s.scoreNodes(state, pod, candidates)

    // 选取得分最高的候选节点（Select）
    sortedCandidates := candidateScores.sort()

    if len(sortedCandidates) == 0 {
        return "", fmt.Errorf("no candidates available for Pod %s", pod.Name)
    }

    // 返回最适合的节点
    return sortedCandidates[0], nil
}

// findCandidateNodes 方法通过寻找所有能够容纳新 Pod 的节点来确定所有候选节点
func (s *MyScheduler) findCandidateNodes(state *schedulerapi.StateData, pod *v1.Pod) ([]string, error) {
    candidates := []string{}
    for node := range state.Nodes.Items {
        if podFitsOnNode(pod, node) {
            candidates = append(candidates, node.Name)
        }
    }
    return candidates, nil
}

// scoreNodes 方法使用自定义的决策规则来为每个候选节点分配分数
func (s *MyScheduler) scoreNodes(state *schedulerapi.StateData, pod *v1.Pod, nodes []string) NodeScoreList {
    scores := []NodeScore{}
    for _, nodeName := range nodes {
        nodeScore := calculateNodeScore(state, pod, nodeName)
        scores = append(scores, NodeScore{nodeName, nodeScore})
    }
    return NodeScoreList(scores)
}

// 将调度器的其他方法定义在这里（如果需要）

// PodFitsOnNode 方法检查 Pod 是否放得下给定节点上
func PodFitsOnNode(pod *v1.Pod, node *v1.Node) bool {
    if len(node.Status.Capacity) == 0 {
        return false
    }
    if node.Status.Capacity.Cpu().MilliValue() < pod.Spec.Containers[0].Resources.Requests.Cpu().MilliValue() {
        return false
    }
    if node.Status.Capacity.Memory().Value() < pod.Spec.Containers[0].Resources.Requests.Memory().Value() {
        return false
    }
    return true
}

// calculateNodeScore 方法为给定的 Pod 和节点计算分数
func calculateNodeScore(state *schedulerapi.StateData, pod *v1.Pod, nodeName string) int {
    // 假设此处计算规则为：节点上所有已分配的 Pod 越少，得分就越高。
    node := state.Nodes.Items[nodeName]
    usedCPU, _ := node.Status.Allocatable.Resources[v1.ResourceCPU]
    usedMemory, _ := node.Status.Allocatable.Resources[v1.ResourceMemory]

    score := node.Status.Capacity.Cpu().MilliValue() - usedCPU.MilliValue()
    score += node.Status.Capacity.Memory().Value() - usedMemory.Value()

    return score
}

// NodeScore 结构体定义了一个候选节点和它的分数
type NodeScore struct {
    Name  string
    Score int
}

// NodeScoreList 是一个 NodeScore 的切片类型，并实现了接口 sort.Interface
type NodeScoreList []NodeScore

// sort 方法将 NodeScoreList 按照分数从高到低排序
func (s NodeScoreList) sort() []string {
    result := []string{}
    set := sets.String{}
    wait.ExponentialBackoff() // 延迟执行
    for len(result) < len(s) {
        for _, ns := range s {
            if ns.Score == -1 {
                continue
            }
            if set.Has(ns.Name) {
                continue
            }
            result = append(result, ns.Name)
            set.Insert(ns.Name)
        }
    }
    return result
}