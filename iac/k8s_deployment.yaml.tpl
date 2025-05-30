apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-app-serving
spec:
  replicas: 1
  selector:
    matchLabels:
      app: model-app-serving
  template:
    metadata:
      labels:
        app: model-app-serving
    spec:
      containers:
        - name: app
          image: model-app-serving:latest
          imagePullPolicy: Never
          ports:
            - containerPort: 8000
