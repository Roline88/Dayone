# DayOne D1 Design Guidelines

## Aesthetic Stance
**Minimalist healthcare** — Clean, reassuring interface prioritizing clarity and trust. Large touch targets, generous spacing, and soft colors create a calm, professional environment for health workers with varying levels of medical training.

## Typography
- **Display**: DM Sans (headings, patient names, key metrics)
- **Body**: DM Sans (all body text, labels, descriptions)
- **Mono**: JetBrains Mono (test results, numerical data, timestamps)

Single humanist sans family for warmth and clarity, with mono reserved for clinical data.

## Color Palette

### Core Colors
- **Background**: Warm off-white (#FAF8F5) — soft, neutral base
- **Foreground**: Deep slate (#1A1A1A) — clear, readable text
- **Card**: Pure white (#FFFFFF) — clean surfaces for patient cards

### Status Colors
- **Green** (#10B981): Stable / Normal — all clear
- **Orange** (#F97316): Monitor closely — needs attention
- **Red** (#EF4444): Urgent / Intervention needed
- **Pastel Blue** (#60A5FA): Primary actions, informational elements
- **Pastel Green** (#86EFAC): Confirmation, success states

### Supporting Colors
- **Muted**: Light warm gray (#F5F5F4) — secondary surfaces
- **Border**: Soft gray (#E7E5E4) — subtle dividers
- **Accent**: Coral (#FB923C) — warnings, important notices

## Layout Principles
1. **Tablet-first**: Designed for 10-12" tablets, large touch targets (minimum 44×44px)
2. **Bottom navigation**: Easy thumb access with 4 primary tabs
3. **Card-based**: Patient records and test results in distinct, scannable cards
4. **Generous spacing**: 24-32px between major sections, 16-20px within cards
5. **Visual hierarchy**: Color-coded status indicators, large readable text, clear CTAs

## Component Patterns
- **Patient cards**: Name, age, status badge, next action, last visit
- **Test cards**: Latest result with mini trend graph, status color, clear CTA
- **Alert cards**: High-contrast warning with immediate action recommendation
- **Checklists**: Large checkboxes with simple, conversational instructions
- **Buttons**: Large (48px height minimum), rounded corners (8px), clear labels

## Data Display
- Use **real, contextually appropriate** placeholder data
- Show numerical results with units prominently
- Include mini trend graphs (sparklines) for test history
- Always pair data with interpretation (Green/Orange/Red + text explanation)

## Accessibility
- AA contrast minimum (4.5:1 for body text, 3:1 for large text)
- Status communicated through color + icon + text
- Large touch targets for field use
- Offline mode indicator and sync status always visible

## Tone
Simple, reassuring, non-clinical language. Avoid medical jargon. Frame everything as clear next steps rather than diagnoses.