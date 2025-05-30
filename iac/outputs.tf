output "node_port_url" {
  value = "http://${chomp(trimspace(data.external.minikube_ip.result["ip"]))}:30001"
  description = "Service URL"
}


data "external" "minikube_ip" {
  program = ["bash", "-c", "echo '{\"ip\": \"'$(minikube ip)'\"}'"]
}