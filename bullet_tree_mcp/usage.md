# Usage

## Parse an outline into JSON

Input:

- Project
  - Tasks
    - Validate collection
    - Add new server
  - Notes
    - Keep it small

Call:

- `bullet_tree_parse(text)`

Output shape:

```json
{
  "indent_size": 2,
  "tree": [
    {
      "text": "Project",
      "children": [
        {
          "text": "Tasks",
          "children": [
            {"text": "Validate collection", "children": []},
            {"text": "Add new server", "children": []}
          ]
        },
        {
          "text": "Notes",
          "children": [
            {"text": "Keep it small", "children": []}
          ]
        }
      ]
    }
  ]
}
```

## Render JSON back to an outline

- `bullet_tree_render(tree_json, bullet='-')`

## Generate stable "paths"

- `bullet_tree_paths(text, sep=' / ')`

Example output:

Project
Project / Tasks
Project / Tasks / Validate collection
Project / Tasks / Add new server
Project / Notes
Project / Notes / Keep it small
