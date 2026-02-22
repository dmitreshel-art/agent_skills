---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
license: Proprietary (based on Anthropic's frontend-design skill)
---

# Frontend Design Skill

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics.

## Skills Path

**Skill Location**: `{workspace}/skills/frontend-design`

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - key is intentionality, not intensity.

## Frontend Aesthetics Guidelines

Focus on:

- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.

- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.

- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use animation libraries for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.

- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.

- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

**NEVER** use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), clichéd color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to your aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing your vision well.

Remember: You are capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

## Technical Implementation

### HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Distinctive Frontend</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <main class="container">
        <header class="hero">
            <h1 class="display-font">Bold Typography</h1>
            <p class="subtitle">Unexpected design choices</p>
        </header>
    </main>
    <script src="app.js"></script>
</body>
</html>
```

### CSS Styling

```css
:root {
    /* Distinctive color palette */
    --primary: #FF6B35;
    --secondary: #004E89;
    --accent: #FFD23F;
    --background: #1A1A1D;
    --text: #FFFFFF;

    /* Typography */
    --font-display: 'Druk Wide', sans-serif;
    --font-body: 'Tiempos', serif;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background: var(--background);
    color: var(--text);
    font-family: var(--font-body);
    overflow-x: hidden;
}

/* Generous negative space */
.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 4rem 2rem;
}

/* Display typography */
.display-font {
    font-family: var(--font-display);
    font-size: clamp(3rem, 8vw, 6rem);
    font-weight: 700;
    line-height: 0.9;
    letter-spacing: -0.02em;
}

/* Sharp accents */
.accent {
    color: var(--accent);
    text-shadow: 0 0 20px rgba(255, 210, 63, 0.5);
}

/* Visual details */
.texture {
    position: fixed;
    inset: 0;
    background:
        radial-gradient(circle at 20% 80%, rgba(255, 107, 53, 0.1) 0%, transparent 50%),
        repeating-linear-gradient(90deg, transparent 0px, transparent 2px, rgba(255,255,255,0.02) 2px);
    pointer-events: none;
    z-index: -1;
}
```

### Animations

```css
/* Page load orchestration */
@keyframes staggerReveal {
    0% {
        opacity: 0;
        transform: translateY(40px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.hero-content > * {
    opacity: 0;
    animation: staggerReveal 0.8s ease-out forwards;
}

.hero-content > *:nth-child(1) { animation-delay: 0s; }
.hero-content > *:nth-child(2) { animation-delay: 0.1s; }
.hero-content > *:nth-child(3) { animation-delay: 0.2s; }

/* Micro-interactions */
button:hover {
    transform: translateX(10px) scale(1.05);
    transition: transform 0.3s cubic-bezier(0.23, 1, 0.32, 1);
}

/* Scroll-triggered animations */
.scroll-reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.8s, transform 0.8s;
}

.scroll-reveal.visible {
    opacity: 1;
    transform: translateY(0);
}
```

## Components

### Hero Section

```html
<section class="hero">
    <div class="hero-content">
        <h1 class="display-font">Unexpected<br>Design</h1>
        <p class="subtitle">Breaking conventions with intentionality</p>
    </div>
    <div class="gradient-mesh"></div>
</section>
```

```css
.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
}

.hero-content {
    z-index: 2;
    text-align: center;
}

.gradient-mesh {
    position: absolute;
    inset: 0;
    background:
        radial-gradient(circle at 30% 20%, var(--accent) 0%, transparent 40%),
        radial-gradient(circle at 70% 80%, var(--primary) 0%, transparent 40%);
    opacity: 0.6;
    filter: blur(60px);
    z-index: 1;
}
```

### Card Components

```html
<div class="card-grid">
    <article class="card">
        <div class="card-image"></div>
        <div class="card-content">
            <h3 class="card-title">Distinctive Card</h3>
            <p class="card-text">Unexpected layout choices</p>
        </div>
    </article>
</div>
```

```css
.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    padding: 4rem;
}

.card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 2rem;
    overflow: hidden;
    transition: transform 0.4s cubic-bezier(0.23, 1, 0.32, 1);
}

.card:hover {
    transform: translateY(-10px);
    border-color: var(--accent);
}

.card-image {
    height: 200px;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    border-radius: 2rem 2rem 0 0;
}
```

## React Implementation

### Styled Components

```jsx
import styled from 'styled-components';

const DisplayHeading = styled.h1`
    font-family: ${props => props.theme.fontDisplay};
    font-size: clamp(3rem, 8vw, 6rem);
    font-weight: 700;
    line-height: 0.9;
    letter-spacing: -0.02em;
    color: ${props => props.theme.background};
`;

const GradientText = styled.span`
    background: linear-gradient(135deg, ${props => props.theme.accent}, ${props => props.theme.primary});
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
`;

function Hero() {
    return (
        <HeroSection>
            <DisplayHeading>
                Unexpected<GradientText>Design</GradientText>
            </DisplayHeading>
        </HeroSection>
    );
}
```

### Animation Libraries

```jsx
import { motion, AnimatePresence } from 'framer-motion';

function PageTransition({ children }) {
    return (
        <AnimatePresence mode="wait">
            <motion.div
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -40 }}
                transition={{ duration: 0.8, ease: [0.23, 1, 0.32, 1] }}
            >
                {children}
            </motion.div>
        </AnimatePresence>
    );
}
```

## Best Practices

### DO
- Commit to a specific aesthetic direction
- Use distinctive fonts and color palettes
- Create visual hierarchy with size and spacing
- Add subtle animations for delight
- Consider accessibility (contrast, keyboard navigation)
- Test on multiple devices
- Optimize for performance

### DON'T
- Use generic templates or layouts
- Converge on common design patterns
- Create cluttered interfaces
- Overanimate without purpose
- Ignore mobile responsiveness
- Use placeholder content
- Skip testing

## Dependencies

- React 18+
- Styled Components 6+
- Framer Motion 10+ (for animations)
- GSAP (for complex animations)
