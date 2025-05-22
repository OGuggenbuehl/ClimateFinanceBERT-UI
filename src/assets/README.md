# CSS Architecture for ClimateFinanceBERT-UI

This document outlines the CSS organization and best practices for the ClimateFinanceBERT-UI project.

## File Structure

- `variables.css`: Design system variables (colors, typography, spacing, etc.)
- `style.css`: Global styles and common components
- `map.css`: Map-specific styles for the interactive map visualization

## Design System

We use CSS variables to maintain a consistent design system. These are defined in `variables.css` and imported where needed.

### Key Variables

- **Colors**: `--color-primary`, `--color-text-light`, etc.
- **Spacing**: `--spacing-xs`, `--spacing-sm`, etc.
- **Shadows**: `--shadow-standard`
- **Typography**: `--font-family-primary`, `--font-size-small`, etc.

## Best Practices

1. **Use CSS variables** for any values that might be reused
2. **Group related styles** in logical sections with comments
3. **Use consistent naming** for classes (kebab-case)
4. **Maintain separation of concerns**:
   - `variables.css` for design tokens
   - `style.css` for global styles
   - Component-specific CSS for specialized components

## Adding New Styles

When adding new styles:

1. Check if there's an existing variable you can use
2. Add styles to the appropriate file based on their scope
3. Consider using the existing class patterns
4. Update this README if you introduce significant new patterns

## Bootstrap Integration

The project uses Bootstrap for some UI components. When working with Bootstrap:

1. Override Bootstrap variables where possible instead of writing new CSS
2. Use the Bootstrap classes for layout and components when available
3. Custom styles should complement, not duplicate Bootstrap functionality
