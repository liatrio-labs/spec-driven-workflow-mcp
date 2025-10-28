# Find Library Usage Command - Generic Template

**Command Name**: `/find-library-usage` (or customize to your preference)

**Purpose**: Search across all services/repositories for usage of a specific shared library, showing real production code examples with file references.

**Token Efficiency**: Uses 5K-15K tokens vs 100K+ tokens for full codebase scan (85-95% reduction)

---

## How It Works

This command launches a specialized agent (enterprise-codebase-documenter or equivalent) with a targeted query to:
1. Grep for library imports/references across all services
2. Read manifest files (package.json, pom.xml, *.csproj, etc.) of matching services
3. Extract 2-3 concrete implementation examples
4. Show configuration patterns
5. Highlight best practices

### Input
User provides library name: `/find-library-usage [LibraryName]`

### Output
Returns:
- List of services using the library (with file:line references)
- 2-3 concrete code examples
- Configuration patterns
- Best practice example

---

## Implementation Guide

### 1. Set Up Enterprise Codebase Documenter Agent

You need an agent that can:
- Search across multiple repositories
- Grep for patterns
- Read specific files
- Generate structured reports

### 2. Create Command Definition

**Command File**: `.claude/commands/find-library-usage.md` (or equivalent)

**Content Structure:**
```markdown
---
description: Find which services use a specific shared library
---

# Find Library Usage Command

You will launch the **enterprise-codebase-documenter** agent to search across all services for usage of a specific shared library.

## Agent Prompt Template

Launch the enterprise-codebase-documenter agent with this prompt:

```
Search across all services (in the [services-directory]/ directory) for usage of [LIBRARY_NAME].

Specifically, find:
1. Which services reference this library (check manifest files)
2. Where the library is used in code (search for imports, interface usage, attribute usage)
3. Concrete code examples showing how it's used
4. Configuration patterns in config files or entry points related to this library

Use targeted query approach (5K-15K tokens), not full scan.

Provide output in this format:
[Output format template]
```

## Usage

User runs: `/find-library-usage [LibraryName]`

Examples:
- `/find-library-usage StorageService`
- `/find-library-usage IQueueConsumer`
- `/find-library-usage @company/auth-lib`
```

### 3. Define Output Format Template

```markdown
# [LibraryName] Usage Analysis

## Services Using This Library (X found)

| Service | Usage Type | Files |
|---------|------------|-------|
| service-a | [role] | path/to/file.ext:45, path/to/config.ext:67 |
| service-b | [role] | path/to/file.ext:120 |
[...more services...]

## Implementation Pattern (Consistent across services)

```[language]
// Example code showing common pattern
```

## Configuration Patterns

[Common configuration approaches observed]

## Best Practice Example

See [service-name]/[path/to/file]:[lines] for complete implementation
with [specific good practices].
```

---

## Example Queries and Responses

### Query: `/find-library-usage IStorageService`

**Response:**
```markdown
# IStorageService Usage Analysis

## Services Using This Library (6 found)

| Service | Usage Type | Files |
|---------|------------|-------|
| document-service | File upload/download | DocumentService.cs:42, DocumentController.cs:78 |
| content-service | Media storage | ContentStorageService.cs:35 |
| asset-service | Asset management | AssetService.cs:56, AssetController.cs:89 |
| backup-service | Backup operations | BackupService.cs:23 |
| report-service | Report storage | ReportGenerator.cs:145 |
| image-service | Image processing | ImageService.cs:67 |

## Implementation Pattern (Consistent across services)

```csharp
// Registration (Startup.cs / Program.cs)
services.AddStorageService(configuration.GetSection("Storage"));

// Usage (Service class)
public class DocumentService
{
    private readonly IStorageService _storageService;

    public DocumentService(IStorageService storageService)
    {
        _storageService = storageService;
    }

    [Traced]
    public async Task<string> UploadDocumentAsync(Stream documentStream, string fileName)
    {
        var storagePath = $"documents/{DateTime.UtcNow:yyyy/MM/dd}/{fileName}";
        var result = await _storageService.UploadAsync(documentStream, storagePath);
        return result.Uri;
    }
}
```

## Configuration Patterns

All services configure storage in `appsettings.json` under `Storage` section:

```json
{
  "Storage": {
    "Provider": "S3",
    "BucketName": "my-app-{environment}",
    "Region": "us-east-1"
  }
}
```

Local development uses `LocalStackEndpoint` override:
```json
{
  "Storage": {
    "LocalStackEndpoint": "http://localhost:4566"
  }
}
```

## Best Practice Example

See **document-service/DocumentService.cs:42-78** for complete implementation including:
- Error handling
- Distributed tracing with [Traced] attribute
- Tenant-aware storage paths
- Stream disposal
- Logging

## Common Variations

**document-service** also includes metadata storage:
```csharp
var uploadResult = await _storageService.UploadAsync(stream, path);
await _repository.SaveMetadataAsync(new DocumentMetadata {
    StoragePath = uploadResult.Uri,
    Size = stream.Length,
    ContentType = contentType
});
```

**Total tokens used: ~9K** (vs 100K+ for full scan)
```

### Query: `/find-library-usage IQueueConsumer`

**Response:**
```markdown
# IQueueConsumer<T> Usage Analysis

## Services Using This Library (8 found)

| Service | Usage Type | Files |
|---------|------------|-------|
| order-processor | Consumer | OrderProcessor.cs:34, Program.cs:56 |
| notification-service | Consumer | NotificationHandler.cs:23, Program.cs:45 |
| analytics-worker | Consumer | AnalyticsProcessor.cs:67, Program.cs:89 |
| email-worker | Consumer | EmailProcessor.cs:45, Program.cs:78 |
| report-generator | Consumer | ReportProcessor.cs:56, Program.cs:90 |
| data-sync-worker | Consumer | DataSyncProcessor.cs:34, Program.cs:67 |
| audit-logger | Consumer | AuditProcessor.cs:23, Program.cs:45 |
| cleanup-worker | Consumer | CleanupProcessor.cs:78, Program.cs:102 |

## Implementation Pattern (Consistent across services)

```csharp
// 1. Create processor class implementing IQueueMessageProcessor<T>
public class OrderProcessor : IQueueMessageProcessor<OrderMessage>
{
    private readonly IOrderService _orderService;
    private readonly ILogger<OrderProcessor> _logger;

    public OrderProcessor(IOrderService orderService, ILogger<OrderProcessor> logger)
    {
        _orderService = orderService;
        _logger = logger;
    }

    [Traced]
    [Metered]
    public async Task ProcessMessageAsync(OrderMessage message, CancellationToken cancellationToken)
    {
        _logger.LogInformation("Processing order {OrderId}", message.OrderId);

        await _orderService.ProcessOrderAsync(message.OrderId);

        _logger.LogInformation("Completed order {OrderId}", message.OrderId);
    }
}

// 2. Register consumer in Program.cs
services.AddQueueConsumer<OrderMessage, OrderProcessor>(options =>
{
    options.QueueUrl = configuration["Queues:OrderQueue"];
    options.MaxConcurrency = 5;
    options.VisibilityTimeoutSeconds = 300;
    options.EnableHeartbeat = true; // For long-running tasks
});

// Background service automatically starts consuming
```

## Configuration Patterns

Queue URLs configured in `appsettings.json`:

```json
{
  "Queues": {
    "OrderQueue": "https://sqs.us-east-1.amazonaws.com/ACCOUNT-ID/order-queue"
  }
}
```

For local development with LocalStack:
```json
{
  "AWS": {
    "LocalStackEndpoint": "http://localhost:4566"
  }
}
```

## Best Practice Example

See **order-processor/OrderProcessor.cs:34-89** for complete implementation including:
- Idempotency handling (check if already processed)
- Error handling with structured logging
- Distributed tracing ([Traced] attribute)
- Metrics collection ([Metered] attribute)
- Graceful cancellation token usage
- Heartbeat for long-running tasks

## Heartbeat Pattern (Long-Running Tasks)

**data-sync-worker** demonstrates heartbeat for tasks > visibility timeout:

```csharp
services.AddQueueConsumer<SyncMessage, DataSyncProcessor>(options =>
{
    options.QueueUrl = configuration["Queues:SyncQueue"];
    options.VisibilityTimeoutSeconds = 300;
    options.EnableHeartbeat = true;
    options.HeartbeatIntervalSeconds = 20;
    options.HeartbeatExtensionSeconds = 90;
});
```

This prevents message redelivery during long processing.

**Total tokens used: ~12K** (vs 100K+ for full scan)
```

---

## Benefits

### For Developers
- **Quick Discovery**: Find real examples in seconds
- **Copy-Paste Ready**: Production code, not docs
- **Best Practices**: See how experienced teams use libraries
- **Configuration Examples**: Real config, not hypothetical

### For Agents
- **Token Efficient**: 5K-15K tokens vs 100K+ full scan
- **Targeted Search**: Grep + selective file reads
- **Structured Output**: Easy to parse and present
- **Real Code**: No hallucination risk

### For Platform Teams
- **Adoption Tracking**: See which services use which libraries
- **Consistency Check**: Identify inconsistent usage patterns
- **Migration Planning**: Know what needs updating
- **Documentation Gap**: Find missing docs when usage varies widely

---

## Common Use Cases

### 1. Developer Starting New Feature
```
Developer: "I need to store files"
Agent: "Let me check what library we use"
Agent runs: `/find-library-usage IStorageService`
Developer: Gets 6 real examples, copies pattern from document-service
Result: Consistent implementation, 30 min saved
```

### 2. Library Deprecation Planning
```
Architect: "We're deprecating OldAuthLib, what's impacted?"
Architect runs: `/find-library-usage OldAuthLib`
Result: List of 12 services that need migration
```

### 3. Code Review
```
Reviewer: "Why not use our queue library?"
Developer: "Didn't know we had one"
Reviewer: `/find-library-usage IQueueConsumer`
Developer: "Oh! Let me refactor"
Result: Prevented duplication
```

### 4. Onboarding
```
New Dev: "How do I integrate with [external service]?"
Mentor: `/find-library-usage [ExternalServiceClient]`
New Dev: Sees 5 examples, understands pattern quickly
Result: Self-service learning
```

---

## Implementation Considerations

### Performance Optimization

**Use Grep for Initial Search:**
```bash
# Fast: Grep for interface/class name
grep -r "IStorageService" --include="*.cs" services/

# Then read only matching files
```

**Don't:**
```bash
# Slow: Read all files looking for usage
cat services/*/src/*.cs  # Reads everything!
```

### Caching

**Cache results for:**
- Recently queried libraries (15 min cache)
- Common libraries (30 min cache)

**Invalidate cache when:**
- Services are deployed
- Manifest files change
- User explicitly requests fresh scan

### Error Handling

**If no usage found:**
```markdown
# [LibraryName] Usage Analysis

## No Usage Found

I searched across all services but found no usage of [LibraryName].

**Possible reasons:**
- Library name misspelled (check exact case)
- Library not yet adopted
- Library deprecated and removed
- Library name changed

**Suggestions:**
- Check library documentation for exact name
- Run `/architecture libraries` to see available libraries
- Check if library is in shared-libraries/ directory
```

---

## Maintenance

### Regular Tasks

**Weekly:**
- [ ] Review cache hit rates
- [ ] Check for failed searches
- [ ] Update common library list

**Monthly:**
- [ ] Validate output format consistency
- [ ] Add newly adopted libraries to tracking
- [ ] Update examples in documentation

**Quarterly:**
- [ ] Review token usage metrics
- [ ] Optimize grep patterns
- [ ] Audit library adoption rates

---

## Success Metrics

Track:
- **Searches per week**: Indicates usefulness
- **Token usage per search**: Should be 5K-15K
- **Cache hit rate**: Should be >40%
- **Time to result**: Should be <30 seconds
- **User satisfaction**: Survey developers

Successful when:
- Developers use it regularly (>20 searches/week)
- Token efficient (average <15K per search)
- Results are actionable
- Reduces code duplication

---

## Customization Checklist

To implement this command for your project:

- [ ] Set up enterprise-codebase-documenter agent
- [ ] Define command in `.claude/commands/` directory
- [ ] Customize output format template
- [ ] Test with 5-10 common libraries
- [ ] Add caching mechanism
- [ ] Create user documentation
- [ ] Add to onboarding materials
- [ ] Monitor usage and optimize
- [ ] Update grep patterns for your tech stack
- [ ] Handle edge cases (no results, multiple patterns, etc.)

---

## Integration with Other Tools

**Works well with:**
- `/architecture [library]` - Get overview before seeing examples
- Implementation guide - Follow examples with detailed docs
- Code review process - Enforce consistent usage

**Example Workflow:**
```
1. `/architecture which library for storage`
   → Learn IStorageService is recommended

2. `/find-library-usage IStorageService`
   → See 6 real examples

3. Copy pattern from document-service
   → Implement with proven pattern

4. Code review
   → Reviewer confirms matches existing usage
```
