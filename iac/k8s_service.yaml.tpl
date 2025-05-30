apiVersion: v1
kind: Service
metadata:
  name: model-app-service
spec:
  type: NodePort
  selector:
    app: model-app-serving
  ports:
    - port: 8000
      targetPort: 8000
      nodePort: 30001
