# Azure Container Apps Cost-Aware Custom Autoscaler
### Automated Resource Optimization with Azure Monitor, Python, and Bicep Infrastructure-as-Code

---
## Execution & Live Behavior Demo

Before I dive into the architectural details and the code breakdown of this project, I want to show exactly how the system behaves under real-world conditions. Below, you can see the live execution output of the autoscaling engine actively monitoring metrics, evaluating thresholds, handling cooldown parameters, and triggering scaling operations in real time.
<table border="0">
  <tr>
    <td><img src="https://github.com/user-attachments/assets/b8bd0c42-75d2-43f7-8f08-9cc6367a92bd" alt="1" width="100%"></td>
    <td><img src="https://github.com/user-attachments/assets/dfacdb71-f1e2-44bd-a3c7-ea4e5e1be222" alt="2" width="100%"></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/3a1f9cbc-c374-430f-859b-09fb7252e9d0" alt="3" width="100%"></td>
    <td><img src="https://github.com/user-attachments/assets/e28d7b27-9695-4649-8363-0e98c0c2d763" alt="4" width="100%"></td>
  </tr>
</table>

During testing, the application initially runs with a single replica. The autoscaler continuously monitors CPU utilization at fixed polling intervals. A single high CPU reading does not immediately trigger scaling because temporary spikes may not represent sustained workload. Instead, the CPU utilization must remain above the configured target (75%) for two consecutive polling cycles before a scale-out operation is performed.

After a new replica is deployed, the autoscaler enters a 60-second cooldown period. This allows the newly created replica to become healthy, traffic to be redistributed, and Azure Monitor to report updated metrics. Once the cooldown expires, monitoring resumes. If CPU utilization remains above the target for another two consecutive polling cycles, an additional replica is created.

Similarly, when CPU utilization remains below the target for consecutive polling cycles, the autoscaler evaluates whether the workload can be handled by fewer replicas. Rather than removing one replica at a time, it estimates the expected CPU utilization for every possible lower replica count and directly selects the minimum safe replica count that keeps CPU utilization below the configured target. This approach minimizes deployment operations while optimizing infrastructure cost.

---

## 1. Introduction & The Business Problem

Whenever I try to book a tatkal ticket on IRCTC, I am always amazed by how the system handles the massive, sudden surge in traffic right when the booking window opens. Within a few minutes, millions of users flood the site, and the demand spikes drastically before normalizing later in the day. Witnessing this firsthand made me incredibly curious about how large-scale applications handle such dynamic behavior. I realized that while building a software application or product can be straightforward, engineering the underlying infrastructure to reliably serve millions of users under extreme stress is the real challenge. If the infrastructure fails during those critical peak minutes, the entire product becomes useless to the world.

This curiosity is what sparked my deep interest in DevOps. However, as I dug deeper into infrastructure management, **I realized that good engineering isn't just about provisioning massive resources to absorb peak traffic; it is equally about managing costs.** A truly resilient, highly available, and scalable system must also be cost-efficient. As engineers, our goal should be to help a company grow toward **profitability** rather than draining its revenue with over-provisioned, idle hardware. I carry this philosophy as my primary goal: **to deliver high-quality infrastructure solutions that balance performance with financial responsibility.**

Driven by this mindset, I was excited to tackle this exact challenge given as assignment  at Kyro. 

Modern cloud applications face constantly shifting workloads, and running a fixed number of container instances either leads to wasted infrastructure costs during low traffic or poor performance during peak hours. 
To solve this, I designed and implemented a custom autoscaling solution for Azure Container Apps.

This implementation demonstrates a custom autoscaling controller to understand the end-to-end scaling workflow.

In a production Azure Container Apps environment, **the preferred approach would be to configure KEDA scale rules (CPU, HTTP, queue-based, etc.)** declaratively using Bicep and allow Azure Container Apps to manage replica scaling natively.
The custom autoscaler implemented in this project is **intended as an educational implementation of the scaling decision process** rather than a replacement for Azure's native autoscaling capabilities.

By continuously monitoring application metrics and evaluating real-time workload conditions, my system automatically adjusts the number of running container replicas using parameterized Bicep templates, successfully balancing high performance with strict cost efficiency.

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Framework | FastAPI |
| Containerization | Docker |
| Cloud | Microsoft Azure |
| Compute | Azure Container Apps |
| Monitoring | Azure Monitor |
| IaC | Bicep |
| Automation | Azure CLI |
| Version Control | Git & GitHub |

---

## 2. What I Learned

This project deepened my understanding of how different Azure services intersect to build an automated, cloud-native solution. Beyond the technical implementation, the most important takeaway was realizing that autoscaling is not just about adding or removing instances—it is a continuous balancing act between application performance and cloud cost.

Through this hands-on engineering challenge, I mastered several key architectural and DevOps concepts:

* **Azure Container Apps & Serverless Compute:** Gained a deep understanding of container deployment lifecycle management and peeked inside the "black box" of how container apps handle orchestration.
* **Azure Monitor Integration:** Learned how to target, collect, and parse real-time application metrics to drive automated infrastructure decisions.
* **Infrastructure as Code (IaC):** Designed and deployed modular, reusable infrastructure blueprints using Bicep templates, i have previously used terraform for infrastructure provisioning.
* **Custom Autoscaling Algorithms:** Designed the core logic to evaluate workload conditions and dynamically calculate required replica counts.
* **System Stability & Flapping Prevention:** Implemented cooldown periods and confirmation counts to prevent rapid, unstable scaling cycles (flapping) during erratic traffic shifts.

---

## 3. Azure Container Apps & Native Scaling

Before starting this project, I knew Azure Container Apps (ACA) as a fully managed, serverless platform that abstracts away Kubernetes and VM management. However, this assignment gave me a valuable opportunity to dive into its underlying architecture and uncover the "black box" of how container scaling actually works.

Natively, ACA handles automatic scaling using **KEDA (Kubernetes Event-driven Autoscaler)**. In a standard deployment, KEDA continuously monitors specific triggers—such as CPU utilization, Memory usage, or HTTP request volume—and automatically scales replicas within defined minimum and maximum boundaries.

To fully understand this entire lifecycle—from raw metric collection to infrastructure deployment—I bypassed the native autoscaler for this assignment and built a custom autoscaling engine from scratch. This hands-on implementation provided deep insights into how cloud platforms dynamically translate system metrics into infrastructure adjustments.

---

## 4. Why Kyro Needs This

I wanted to understand how this project applies to Kyro.ai. Looking into their services, they specialize in Field Service Management for massive, heavy-duty industries like electric utilities, construction, and storm restoration. Their AI platform replaces outdated paperwork to connect field workers (like linemen) with back-office management. A fixed infrastructure simply cannot handle their highly volatile workloads:

* **Handling Extreme Surges:** During a crisis like a storm or wildfire, thousands of linemen must log in simultaneously. Similarly, during the day, construction managers heavily load the system uploading massive drone files or generating billing invoices, pushing CPU/Memory to 90%. If the system doesn't spin up replicas immediately, it crashes—leading to catastrophic communication failures that can cause real physical and environmental danger.
* **Eliminating Wasted Capital:** Conversely, at 2:00 AM when nobody is using the platform, keeping 5 container instances running means Kyro is wasting money paying Microsoft for idle hardware. The system needs to automatically kill unused instances down to a bare minimum.

Building a custom autoscaling engine instead of relying on default cloud rules gives Kyro precise operational and financial control. It allows the organization to:

* **Optimize Azure Infrastructure Costs:** Dramatically reduce spend by cutting out idle hardware.
* **Guarantee High Availability:** Automatically respond to critical workload changes so the system never fails field workers.
* **Embed Custom Business Logic:** Customize scaling policies and decision metrics specifically tailored to heavy-industry operational requirements.

---

## 5. Architecture

### 6.5.4 System Workflow Architecture

The sequential automation loop for the orchestration engine is outlined in the diagram below:

```text
                 Start Autoscaler
                        │
                        ▼
              Collect Azure Metrics
                        │
                        ▼
         Retrieve Current Replica Count
                        │
                        ▼
            Evaluate Scaling Decision
                        │
         ┌──────────────┴──────────────┐
         │                             │
         ▼                             ▼
  No Scaling Required          Scaling Required
         │                             │
         │                             ▼
         │                 Deploy Updated Bicep
         │                             │
         └──────────────┬──────────────┘
                        ▼
             Wait Monitoring Interval
                        │
                        ▼
                  Repeat Process
```

The autoscaler continuously monitors the Azure Container App, evaluates the collected metrics, decides whether scaling is required, and updates the application by redeploying the Bicep template with the new replica configuration.

---

## 6. Implementation

### Branching Strategy

```text
main
│
├
│     
|── feature/cli-metrics
```

To maintain a structured, production-grade development workflow, I adopted a feature-branch strategy:

* **main Branch:** Stores only stable, production-ready code.
* **feature/cli-metrics Branch:** Served as my isolated playground to develop, test, and refine new features (like Azure CLI metric collection) without risking breaking the stable codebase.

Once features were fully validated, I used Pull Requests to safely merge the changes back into the main branch.

### Application

To demonstrate the autoscaling behavior in container apps, we require a docker image that runs any application so  I developed a lightweight FastAPI application and containerized it using Docker before deploying it to Azure Container Apps.

#### Why Docker?
Docker packages the application along with all its dependencies into a single container image. This ensures that the application runs consistently across local and cloud environments without any configuration differences.

#### REST Endpoints
The application exposes two REST endpoints:

#### 1. `/site-safety`
A simple endpoint that simulates a normal application request to verify successful deployment, test application availability, and generate regular traffic.

**Example Request:**
```http
GET /site-safety
{
    "company": "KYRO AI Operations",
    "site_status": "Clear Skies - Safe to Work",
    "monitoring": "Active"
}
```
#### 2. `/stress`
This endpoint intentionally performs CPU-intensive operations to increase processor utilization, simulate high workloads, generate CPU spikes, trigger the custom autoscaler, and validate scale-out and scale-in decisions.

Without this endpoint, generating sufficient CPU utilization to test the scaling algorithm would be difficult. During testing, repeated requests to `/stress` increased CPU usage beyond the configured threshold, allowing the autoscaler to detect sustained load and provision additional replicas automatically.

**Note:** I intentionally kept the application simple because the focus of this assignment is the autoscaling system, not the application itself. The FastAPI service serves as a workload generator to validate the custom scaling logic under different traffic conditions.


### Azure Container Apps Setup

The application was deployed to Azure Container Apps using a combination of Azure CLI and Bicep. Azure CLI was used for resource creation and deployment, while Bicep was used to define the infrastructure in a reusable and parameterized manner.
The overall deployment involved the following steps:
	1. Create an Azure Resource Group. 
	2. Create an Azure Container Registry (ACR). 
	3. Build the Docker image and push it to ACR. 
	4. Create an Azure Container Apps Environment. 
	5. Deploy the Container App using a Bicep template. 
	6. Configure the application to pull images from ACR using a User Assigned Managed Identity. 
This approach keeps the infrastructure reproducible and allows replica configurations to be updated automatically by the autoscaler.


### Components


### monitor_cli.py

**Responsibility**
Collects application telemetry and performance metrics from Azure Monitor.

**Inputs**
* Azure Resource ID
* Target Metric Names (`cpu`, `memory`, etc.)

**Outputs**
* CPU Utilization
* Memory Utilization
* Request Count

**Azure CLI Command Used**
```
az monitor metrics list
```
**Design Decision: Why Azure CLI instead of Azure SDK?**

For this project, I prioritized **Azure CLI** over the Azure SDK to minimize configuration overhead and focus purely on the autoscaling logic.

* **Zero Dependency Overhead:** Avoids heavy Python SDK library management and versioning.
* **Unified Authentication:** Reuses active system-level CLI sessions (`az login`) automatically.
* **Rapid Debugging:** Commands can be tested directly in the terminal before script integration.
* **Objective-Focused:** Provides a straightforward, lightweight shortcut for metric extraction without enterprise pipeline complexity.

### scaler.py

This is the **core decision engine** of the project. It receives the collected metrics and determines whether the application should scale in, scale out, or maintain its current state.

The scaler implements several mechanisms to ensure stable scaling decisions:

* **Scale Out:** When CPU utilization remains above the configured target for multiple consecutive checks, the autoscaler adds **one replica**. Scaling out one replica at a time avoids sudden over-provisioning and allows the system to gradually respond to increasing traffic.
* **Scale In:** Instead of removing one replica at a time, the scaler estimates the CPU utilization for every possible lower replica count using the formula:
* 
  $$\text{Expected CPU} = \frac{\text{Current CPU} \times \text{Current Replicas}}{\text{Candidate Replicas}}$$


  The first replica count whose expected CPU remains below the target threshold is selected. This allows the autoscaler to directly scale to the **minimum safe replica count**, reducing unnecessary intermediate deployments and lowering infrastructure costs. Compared to reducing one replica at a time, this approach reaches the optimal state faster while minimizing deployment operations.
* **Cooldown:** After every scaling operation, the autoscaler waits for a configurable cooldown period before making another scaling decision. This gives the application enough time to stabilize and allows Azure Monitor to report updated metrics. Without a cooldown period, the autoscaler might react to stale metrics and perform unnecessary scaling actions.
* **Confirmation Count:** A single CPU spike should not immediately trigger scaling. To prevent this, scaling decisions are made only after the CPU threshold is exceeded (or remains below the threshold) for a configurable number of consecutive monitoring cycles. This reduces false scaling decisions caused by temporary traffic spikes.

### Why Scale-to-Zero was not implemented

Azure Container Apps support **scale-to-zero** through KEDA, where the application is activated by an event such as an HTTP request, queue message, or other supported triggers.

In this project, I implemented a **CPU-based custom autoscaler**. Since CPU metrics are available only when at least one container instance is running, scaling down to zero would leave no running instance to generate utilization metrics. As a result, the autoscaler would have no information to determine when the application should scale back up.

To ensure continuous monitoring and autonomous scaling decisions, I configured the minimum replica count as **1**. In a production implementation, scale-to-zero would typically be achieved using KEDA's event-driven scaling rules rather than a polling-based CPU autoscaler.

 ---

#### Preventing Flapping (Oscillation)

One common challenge in autoscaling systems is **flapping** (also known as oscillation), which occurs when the application repeatedly scales out and scales in because the CPU utilization fluctuates tightly around the threshold. 

The autoscaler minimizes this behavior using a combination of guards:
1. Cooldown periods
2. Confirmation counts
3. Separate scale-out and scale-in logic
4. Predictive scale-in calculations

These mechanisms ensure that scaling decisions are based on sustained workload changes rather than temporary metric fluctuations.

### replica.py

The replica.py component retrieves the current configured replica count of the Azure Container App.

Initially, I attempted to obtain replica information from Azure Monitor. However, Azure Monitor reports the average number of replicas over a time interval rather than the actual configured replica count. This produced values such as 1.45, which were unsuitable for making scaling decisions.

To obtain the exact replica count, I used the Azure CLI.

**Azure CLI Command Used**
```
az containerapp show \
  --name <container-app-name> \
  --resource-group <resource-group>
```

The command returns the current Container App configuration, from which the configured replica count is extracted.

### azure_scale.py

This component is responsible for applying the scaling decision to Azure.
Instead of directly updating the Container App configuration, the autoscaler redeploys the existing Bicep template with the updated replica count.

The deployment is performed using:

**Azure CLI Command Used**
```
az deployment group create \
    --resource-group <resource-group> \
    --template-file deploy.bicep \
    --parameters minReplicas=<value> maxReplicas=<value>
```

By reusing the same Infrastructure as Code template, the application configuration remains consistent and version-controlled. The autoscaler only changes the replica configuration while the remaining infrastructure stays unchanged.

### main.py

The main.py file acts as the orchestrator of the autoscaling system.

It continuously performs the following tasks:

- Collect metrics from Azure Monitor.
- Retrieve the current replica count.
- Pass the collected information to the scaling engine.
- Deploy updated infrastructure if scaling is required.
- Wait for the configured monitoring interval.
- Repeat the process.

Since all components are independent, main.py only coordinates the workflow without containing any business logic.


### Bicep

I defined the entire infrastructure for this project using Bicep, Microsoft's domain-specific language for Infrastructure as Code (IaC). Instead of clicking through the portal, I used this template to declaratively provision and configure everything.

The Bicep template handles the complete setup of:

- Azure Container App: The core serverless container hosting environment.
- User-Assigned Managed Identity: Securing access without managing hardcoded credentials.
- Azure Container Registry Authentication: Allowing the Container App to securely pull the deployment images.
- Cntainer Image & Resource Allocation: Defining the specific images to run and their allocated CPU/Memory resources.
- Replica Configuration: Setting up the operational scaling boundaries.

**How it fits together:**
I designed this template to be fully parameterized. When my custom autoscaler determines that a scaling action is needed, it simply passes the new target replica counts as parameters during deployment. This allows me to reuse the exact same infrastructure template for every single scaling operation, making sure the environment's state stays consistent and predictable.

---

## 7. Future Enhancements

What I found to be a major drawback in this system is that when I shut down my laptop or close my code editor, the autoscaler stops fetching metrics and scaling the replicas. Currently, it is written inside an infinite while loop that only works as long as I am online and my local machine is running.

To make the system highly available and production-ready, I want to implement the following enhancements:
- Transition to Azure Functions: I plan to move the autoscaler from a locally running script to an Azure Function with a Timer Trigger. This will allow it to run every 30 seconds automatically in a fully managed, serverless cloud environment, watching the system 24/7 without needing my laptop to be on.
- Persistent State Management: Since Azure Functions are serverless and stateless, I need to store my cooldown timers and confirmation counters in Azure Blob Storage or Table Storage so that the autoscaler can safely recover its state across executions and restarts.
- Multi-Metric Scaling Matrices: I want to upgrade the core logic to make scaling decisions based on a combination of CPU, memory utilization, and request counts together, rather than relying primarily on just CPU metrics.

---

## 8. Conclusion

This project demonstrates a custom autoscaling solution for Azure Container Apps using Azure Monitor, Python, Azure CLI and Bicep. The implementation balances application performance, stability and infrastructure cost through a modular and maintainable design.
