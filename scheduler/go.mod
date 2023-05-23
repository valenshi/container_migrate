module sample-scheduler-framework

go 1.13

require (
	golang.org/x/text v0.3.3 // indirect
	k8s.io/api v0.18.8
	k8s.io/apimachinery v0.18.8
	k8s.io/apiserver v0.18.8 // indirect
	k8s.io/component-base v0.0.0
	k8s.io/klog v1.0.0
	// k8s.io/kube-openapi v0.0.0-20200410145947-61e04a5be9a6 // indirect
	k8s.io/kubernetes v1.27.2
)

replace (
	k8s.io/api => /root/go/kubernetes-1.18.8/staging/src/k8s.io/api
	k8s.io/apiextensions-apiserver => /root/go/kubernetes-1.18.8/staging/src/k8s.io/apiextensions-apiserver
	k8s.io/apimachinery => /root/go/kubernetes-1.18.8/staging/src/k8s.io/apimachinery
	k8s.io/apiserver => /root/go/kubernetes-1.18.8/staging/src/k8s.io/apiserver
	k8s.io/cli-runtime => /root/go/kubernetes-1.18.8/staging/src/k8s.io/cli-runtime
	k8s.io/client-go => /root/go/kubernetes-1.18.8/staging/src/k8s.io/client-go
	k8s.io/cloud-provider => /root/go/kubernetes-1.18.8/staging/src/k8s.io/cloud-provider
	k8s.io/cluster-bootstrap => /root/go/kubernetes-1.18.8/staging/src/k8s.io/cluster-bootstrap
	k8s.io/code-generator => /root/go/kubernetes-1.18.8/staging/src/k8s.io/code-generator
	k8s.io/component-base => /root/go/kubernetes-1.18.8/staging/src/k8s.io/component-base
	k8s.io/cri-api => /root/go/kubernetes-1.18.8/staging/src/k8s.io/cri-api
	k8s.io/csi-translation-lib => /root/go/kubernetes-1.18.8/staging/src/k8s.io/csi-translation-lib
	k8s.io/kube-aggregator => /root/go/kubernetes-1.18.8/staging/src/k8s.io/kube-aggregator
	k8s.io/kube-controller-manager => /root/go/kubernetes-1.18.8/staging/src/k8s.io/kube-controller-manager
	k8s.io/kube-proxy => /root/go/kubernetes-1.18.8/staging/src/k8s.io/kube-proxy
	k8s.io/kube-scheduler => /root/go/kubernetes-1.18.8/staging/src/k8s.io/kube-scheduler
	k8s.io/kubectl => /root/go/kubernetes-1.18.8/staging/src/k8s.io/kubectl
	k8s.io/kubelet => /root/go/kubernetes-1.18.8/staging/src/k8s.io/kubelet
	k8s.io/kubernetes => /root/go/kubernetes-1.18.8
	k8s.io/legacy-cloud-providers => /root/go/kubernetes-1.18.8/staging/src/k8s.io/legacy-cloud-providers
	k8s.io/metrics => /root/go/kubernetes-1.18.8/staging/src/k8s.io/metrics
	k8s.io/sample-apiserver => /root/go/kubernetes-1.18.8/staging/src/k8s.io/sample-apiserver
)
