# Director Workspace UI source seam

This directory is reserved by B0.0B; it contains no UI runtime yet and is not
served by the existing Backlot application.

Future modules here must consume `/api/workspace/v1` projections. They must not
import the legacy Board state modules, call legacy project-state endpoints,
construct raw project/media paths, or parse canonical/private production files.
B0.2 must register this UI conditionally so the complete Workspace surface is
404 when its default-off feature flag is disabled. The existing Board files in
`backlot/ui/` remain unchanged.
