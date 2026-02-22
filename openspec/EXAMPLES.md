# OpenSpec Usage Examples

Real-world examples of using the OpenSpec SDD methodology.

## Example 1: Adding Dark Mode to a React App

### Start the Change

```
You: /opsx:new add-dark-mode

AI: Created openspec/changes/add-dark-mode/
     Schema: spec-driven
     Ready to create: proposal
```

### Create All Planning Artifacts

```
You: /opsx:ff

AI: Creating artifacts for add-dark-mode...
     ✓ proposal.md — why we're doing this, what's changing
     ✓ specs/ — requirements and scenarios
     ✓ design.md — technical approach
     ✓ tasks.md — implementation checklist
     Ready for implementation!
```

### What Gets Created

**proposal.md:**
```markdown
# Proposal: Add Dark Mode

## Intent
Users have requested a dark mode option to reduce eye strain
during nighttime usage and match system preferences.

## Scope

In scope:
- Theme toggle in settings
- System preference detection
- Persist preference in localStorage

Out of scope:
- Custom color themes (future work)
- Per-page theme overrides

## Approach
Use CSS custom properties for theming with a React context
for state management. Detect system preference on first load,
allow manual override.
```

**specs/ui/spec.md:**
```markdown
# Delta for UI

## ADDED Requirements

### Requirement: Theme Selection
The system SHALL allow users to choose between light and dark themes.

#### Scenario: Manual toggle
- GIVEN a user on any page
- WHEN the user clicks the theme toggle
- THEN the theme switches immediately
- AND the preference persists across sessions

#### Scenario: System preference
- GIVEN a user with no saved preference
- WHEN the application loads
- THEN the system's preferred color scheme is used
```

**tasks.md:**
```markdown
# Tasks

## 1. Theme Infrastructure
- [ ] 1.1 Create ThemeContext with light/dark state
- [ ] 1.2 Add CSS custom properties for colors
- [ ] 1.3 Implement localStorage persistence
- [ ] 1.4 Add system preference detection

## 2. UI Components
- [ ] 2.1 Create ThemeToggle component
- [ ] 2.2 Add toggle to settings page
- [ ] 2.3 Update Header to include quick toggle

## 3. Styling
- [ ] 3.1 Define dark theme color palette
- [ ] 3.2 Update components to use CSS variables
- [ ] 3.3 Test contrast ratios for accessibility
```

### Implement

```
You: /opsx:apply

AI: Implementing add-dark-mode...
     Working on 1.1: Create ThemeContext...
     ✓ 1.1 Complete
     Working on 1.2: Add CSS custom properties...
     ✓ 1.2 Complete
     ...
     All tasks complete!
```

### Archive

```
You: /opsx:archive

AI: Archiving add-dark-mode...
     ✓ Synced specs to openspec/specs/ui/spec.md
     ✓ Moved to openspec/changes/archive/2025-01-24-add-dark-mode/
     Done! Ready for the next feature.
```

## Example 2: Fixing a Login Redirect Bug

### Start and Fast-Forward

```
You: /opsx:new fix-login-redirect
AI: Created openspec/changes/fix-login-redirect/

You: /opsx:ff
AI: ✓ Created proposal.md
     ✓ Created specs/auth/spec.md
     ✓ Created design.md
     ✓ Created tasks.md
```

**proposal.md:**
```markdown
# Proposal: Fix Login Redirect Bug

## Intent
Users are being redirected to the wrong page after successful login.
Currently redirects to home, should redirect to the intended destination.

## Scope

In scope:
- Fix redirect logic in auth handler
- Add unit tests for redirect scenarios

Out of scope:
- General auth flow refactoring

## Approach
Store the intended destination in a query parameter during auth redirect,
read it after successful login, default to dashboard if not present.
```

**specs/auth/spec.md:**
```markdown
# Delta for Auth

## MODIFIED Requirements

### Requirement: Post-Login Redirect
The system SHALL redirect users to the intended destination after successful login.
(Previously: redirected to home page)

#### Scenario: Redirect to intended page
- GIVEN a user tries to access /dashboard/settings
- WHEN the user is redirected to login
- AND successfully authenticates
- THEN the user is redirected to /dashboard/settings

#### Scenario: Default to dashboard
- GIVEN a user directly navigates to /login
- WHEN the user successfully authenticates
- THEN the user is redirected to /dashboard
```

### Quick Implementation

```
You: /opsx:apply

AI: Implementing fix-login-redirect...
     ✓ 1.1 Added redirectUrl query parameter to auth redirect
     ✓ 1.2 Updated login handler to use redirectUrl
     ✓ 2.1 Added unit test for redirect scenario
     ✓ 2.2 Added unit test for default redirect
     All tasks complete!

You: /opsx:archive

AI: ✓ Archived fix-login-redirect
```

## Example 3: Exploratory Development

### Explore the Problem

```
You: /opsx:explore

AI: What would you like to explore?

You: I want to improve page load performance but I'm not sure
     where the bottlenecks are.

AI: Let me help investigate...
     [Analyzes bundle sizes, identifies slow queries, reviews
     component render patterns]

     I found three main bottlenecks:
     1. Large unoptimized images (average 2.3MB)
     2. Synchronous data fetching in ProductList component
     3. Re-renders from context changes

     Which would you like to address first?
```

### Start the Change

```
You: Let's tackle the data fetching issue.

You: /opsx:new optimize-product-list-fetching

AI: Created openspec/changes/optimize-product-list-fetching/
     Ready to create: proposal

You: /opsx:continue

AI: Creating proposal based on our exploration...
     ✓ Created proposal.md (includes analysis findings)
     Ready to create: specs, design
     Which would you like next?

You: /opsx:continue

AI: Creating specs...
     ✓ Created specs/api/spec.md
     Now available: tasks

You: /opsx:ff

AI: ✓ Created design.md
     ✓ Created tasks.md
     Ready for implementation!
```

## Example 4: Parallel Changes

### Work on Multiple Changes

```
You: I'm working on add-dark-mode but got pulled into a bug fix

You: /opsx:new fix-login-redirect

AI: Created openspec/changes/fix-login-redirect/

You: /opsx:ff

AI: ✓ Created planning artifacts for fix-login-redirect

You: /opsx:apply

AI: Working on fix-login-redirect...
     [Implements the fix]
     All tasks complete!

You: /opsx:archive

AI: ✓ Archived fix-login-redirect

You: Let's get back to dark mode

You: /opsx:apply add-dark-mode

AI: Resuming add-dark-mode...
     Picking up at task 2.3: Update Header...
```

### Bulk Archive Multiple Changes

```
You: /opsx:bulk-archive

AI: Found 3 completed changes:
     - add-dark-mode (8/8 tasks complete)
     - fix-login-redirect (3/3 tasks complete)
     - update-footer (2/2 tasks complete)

     Checking for spec conflicts...
     ⚠ add-dark-mode and update-footer both touch specs/ui/

     Inspecting codebase to resolve...
     Both changes are implemented. Will apply in chronological order.

     Archive all 3 changes?

You: Yes

AI: ✓ Archived add-dark-mode
     ✓ Archived fix-login-redirect
     ✓ Archived update-footer
     Specs merged in order: add-dark-mode → update-footer
```

## Example 5: Updating an Existing Change

### When Learning Reveals New Information

```
You: /opsx:apply add-dark-mode

AI: Working on task 1.4: Add system preference detection...
     [Attempts to implement]
     ⚠ System preference detection requires MediaQueryListener
     but this isn't available in the current React version (16.8).
     Need to update approach.

You: Update the design and continue

AI: Updating design.md...
     Changed approach to use window.matchMedia() with
     useEffect-based listener instead of MediaQueryListener.

     Updated tasks.md:
     - [ ] 1.4 Use window.matchMedia() with useEffect for detection
     - [ ] 1.5 Add cleanup for event listeners

     Continuing implementation...
     ✓ 1.4 Complete
     ✓ 1.5 Complete
```

## Example 6: Verification Before Archiving

### Check Implementation Quality

```
You: /opsx:verify

AI: Verifying add-auth...

     COMPLETENESS
     ✓ All 12 tasks in tasks.md are checked
     ✓ All requirements in specs have corresponding code
     ⚠ Scenario "Session timeout after inactivity" not tested

     CORRECTNESS
     ✓ Implementation matches spec intent
     ✓ Edge cases from scenarios are handled
     ✓ Error states match spec definitions

     COHERENCE
     ✓ Design decisions reflected in code structure
     ✓ Naming conventions consistent with design.md
     ⚠ Design mentions "event-driven" but implementation uses polling

     SUMMARY
     ─────────────────────────────
     Critical issues: 0
     Warnings: 2
     Ready to archive: Yes (with warnings)

     Recommendations:
     1. Add test for session timeout scenario
     2. Consider refactoring to event-driven as designed, or update design.md
```

## Key Takeaways

1. **Use `/opsx:ff`** when you know what to build — creates all artifacts at once
2. **Use `/opsx:continue`** when exploring — create artifacts step by step
3. **Use `/opsx:explore`** before starting — investigate unclear requirements
4. **Use `/opsx:verify`** before archiving — catch implementation issues
5. **Update artifacts** when you learn — designs and specs can evolve
6. **Bulk archive** parallel changes — handles conflicts intelligently

## Workflow Summary

```
Quick Feature:   /opsx:new → /opsx:ff → /opsx:apply → /opsx:verify → /opsx:archive
Exploratory:     /opsx:explore → /opsx:new → /opsx:continue → ... → /opsx:apply
Parallel work:   Switch context with /opsx:apply <change-name>
Multiple done:   /opsx:bulk-archive
```

These examples show the most common patterns. For complete command reference, see [SKILL.md](./SKILL.md).
