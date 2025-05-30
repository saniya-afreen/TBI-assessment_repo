provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_deployment" "model-app" {
  metadata {
    name = "model-app-serving"
    labels = {
      app = "model-app-serving"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "model-app-serving"
      }
    }

    template {
      metadata {
        labels = {
          app = "model-app-serving"
        }
      }

      spec {
        container {
          name  = "model-app-serving"
          image = var.image_name
          image_pull_policy = "Never"

          port {
            container_port = 8000
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "model-app-service" {
  metadata {
    name = "model-app-service"
  }

  spec {
    type = "NodePort"
    selector = {
      app = "model-app-serving"
    }

    port {
      port        = 8000
      target_port = 8000
      node_port   = 30001
    }
  }
}
