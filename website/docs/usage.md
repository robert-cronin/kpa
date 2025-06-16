---
sidebar_position: 3
title: Usage Guide
---

# Usage Guide

Learn how to effectively use the Kubernetes Practice Assistant to enhance your Kubernetes skills.

## Getting Started with KPA

### Accessing the Application

Once KPA is running, navigate to `http://localhost:8080` in your web browser. You'll see the main interface with available scenarios.

### Understanding the Interface

The KPA interface consists of:

1. **Scenario Selection Page** (`/`)
   - Browse available practice scenarios
   - Filter by difficulty level
   - Track your progress

2. **Scenario Page** (`/scenario/<id>`)
   - Interactive terminal with kubectl access
   - AI chat assistant
   - Task objectives and hints

## Working with Scenarios

### Available Scenarios

KPA includes various scenarios covering:
- **Basic Operations**: Pod creation, deployment management
- **Troubleshooting**: Debugging failed deployments, fixing configurations
- **Networking**: Service configuration, ingress setup
- **Storage**: PersistentVolume and PersistentVolumeClaim management
- **Security**: RBAC, NetworkPolicies, SecurityContexts
- **Advanced Topics**: StatefulSets, DaemonSets, Jobs, CronJobs

### Starting a Scenario

1. **Select a Scenario**: Click on any scenario from the home page
2. **Read the Objectives**: Each scenario displays clear objectives
3. **Use the Terminal**: Execute kubectl commands in the web terminal
4. **Get AI Assistance**: Ask questions in the chat panel

### Example Workflow

Let's walk through a typical scenario:

```bash
# Scenario: Create and expose a deployment

# 1. Create a deployment
kubectl create deployment nginx --image=nginx:latest --replicas=3

# 2. Check the deployment status
kubectl get deployments
kubectl get pods

# 3. Expose the deployment as a service
kubectl expose deployment nginx --port=80 --type=ClusterIP

# 4. Verify the service
kubectl get services
kubectl describe service nginx
```

## Using the AI Assistant

### Effective Prompting

The AI assistant can help you with:
- **Explaining concepts**: "What is a Kubernetes Service?"
- **Debugging help**: "Why is my pod in CrashLoopBackOff?"
- **Command assistance**: "How do I scale a deployment?"
- **Best practices**: "What's the best way to handle secrets?"

### Example Interactions

```text
You: My pod is stuck in Pending state. How can I debug this?

AI: To debug a pod stuck in Pending state, follow these steps:
1. Check pod events: kubectl describe pod <pod-name>
2. Look for scheduling issues, resource constraints, or node selectors
3. Check node resources: kubectl describe nodes
4. Verify if PersistentVolumeClaims are bound
...
```

## Terminal Features

### Supported Commands

The web terminal supports most kubectl commands:
- `kubectl get/describe/create/delete/edit`
- `kubectl logs`
- `kubectl exec`
- `kubectl port-forward`
- Basic shell commands: `ls`, `cat`, `echo`, etc.

### Keyboard Shortcuts

- **Ctrl+C**: Cancel current command
- **Ctrl+L**: Clear terminal
- **Tab**: Auto-completion (where available)
- **↑/↓**: Navigate command history

## Tips for Success

### 1. Practice Systematically

- Start with beginner scenarios
- Complete each scenario thoroughly
- Review solutions after completion
- Retry scenarios to improve speed

### 2. Use the AI Wisely

- Ask for hints, not complete solutions
- Request explanations for concepts you don't understand
- Use it to verify your approach

### 3. Learn from Mistakes

- Don't worry about breaking things - it's a safe environment
- Experiment with different approaches
- Review error messages carefully

### 4. Track Your Progress

- Complete scenarios in order
- Note areas where you struggle
- Return to challenging scenarios

## Advanced Features

### Custom Scenarios

You can create custom scenarios by:

1. Defining scenario objectives
2. Setting up initial cluster state
3. Creating validation checks

### Keyboard Navigation

- **Alt+T**: Focus terminal
- **Alt+C**: Focus chat
- **Esc**: Exit focus mode

### Session Management

- Sessions are automatically saved
- You can resume scenarios where you left off
- Progress is tracked in the local database

## Common Use Cases

### CKA/CKAD Exam Preparation

1. **Time yourself**: Practice scenarios within exam time limits
2. **No external resources**: Try solving without documentation
3. **Focus on speed**: Improve command execution efficiency
4. **Cover all domains**: Ensure you practice all exam objectives

### Team Training

1. **Share scenarios**: Export and import custom scenarios
2. **Track team progress**: Monitor completion rates
3. **Collaborative learning**: Discuss solutions with teammates

### Skill Assessment

1. **Benchmark performance**: Track completion times
2. **Identify weak areas**: Focus on challenging topics
3. **Regular practice**: Maintain and improve skills

## Troubleshooting Common Issues

### Terminal Not Responding

```bash
# Refresh the page
# Check browser console for errors
# Ensure WebSocket connection is active
```

### Commands Not Working

```bash
# Verify kubectl is properly configured
kubectl version

# Check cluster connection
kubectl cluster-info
```

### AI Assistant Issues

- Ensure OpenAI API key is configured
- Check for rate limiting
- Verify internet connectivity

## Next Steps

- [Installation](./installation) - Installation instructions