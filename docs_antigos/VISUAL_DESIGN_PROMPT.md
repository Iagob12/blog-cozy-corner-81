# 🎨 PROMPT VISUAL PERFEITO - Alpha Terminal

## Para Designers ou IA de Design (Midjourney, DALL-E, etc.)

---

## 🎯 PROMPT PRINCIPAL

```
Design a modern financial terminal dashboard with cyberpunk-minimalist aesthetic.

STYLE REFERENCES:
- Bloomberg Terminal (professional financial interface)
- Cyberpunk 2077 UI (neon accents, dark theme)
- Apple Design System (clean, minimal, elegant)
- Stripe Dashboard (modern SaaS interface)

COLOR PALETTE:
- Background: Deep black (#0a0a0f) with subtle blue gradient
- Primary accent: Neon green (#00ff88) for positive/buy signals
- Secondary accent: Electric red (#ff3366) for alerts/sell signals
- Warning: Gold yellow (#ffd700) for caution
- Text: Pure white (#ffffff) with gray variants for hierarchy
- Borders: Subtle white glow (rgba(255,255,255,0.1))

LAYOUT:
- Bento Grid system (asymmetric card layout)
- Hero card (2 columns wide) featuring "Alpha Pick of the Day"
- Sidebar (1 column) with real-time alerts feed
- Full-width table below showing 15 elite stocks
- Top bar with macro indicators (interest rates, inflation)

TYPOGRAPHY:
- Headers: Inter Bold, 24-32px
- Body: Inter Regular, 14-16px
- Numbers/Data: JetBrains Mono, 16-20px (monospace for alignment)
- Accent text: Inter SemiBold, 12-14px

VISUAL EFFECTS:
- Glassmorphism: Subtle frosted glass effect on cards
- Glow effects: Neon green glow on hover (box-shadow: 0 0 20px rgba(0,255,136,0.3))
- Micro-animations: Smooth transitions (200ms ease-out)
- Gradient overlays: Subtle radial gradients on backgrounds
- Depth: Layered cards with elevation shadows

COMPONENTS TO DESIGN:

1. HERO CARD - "Alpha Pick of the Day"
   - Large ticker symbol (48px, bold)
   - Company name and sector badge
   - Current price vs ceiling price with progress bar
   - Upside percentage in large green text
   - Catalyst tags with icons (🚀 expansion, 📝 contract)
   - Efficiency score gauge (circular progress)
   - "BUY STRONG" badge with pulse animation
   - Sentiment indicator (😊 normal, ⚠️ caution, 🚨 alert)
   - "View Full Thesis" button with arrow

2. ALERTS FEED (Sidebar)
   - Compact cards with colored left border
   - Icon + ticker + message + timestamp
   - Green border: Buy opportunity
   - Red border: Take profits
   - Yellow border: Herd risk warning
   - Slide-in animation from right

3. ELITE TABLE
   - Dark background with subtle grid lines
   - Hover effect: Row highlights with glow
   - Sortable columns with arrow indicators
   - Colored badges for sectors
   - Trend icons (↑ up, ↓ down)
   - Sparkline mini-charts in last column
   - Sticky header on scroll

4. MACRO BAR (Top)
   - Horizontal layout with icons
   - Interest rate icon + value
   - Inflation icon + value
   - Favored sectors with checkmarks
   - Pulse animation on data update

5. THESIS PANEL (Slide-out)
   - Full-height sidebar from right
   - Sections: Fundamentals, Entry Strategy, Catalysts, Macro Context, Risks
   - Collapsible accordions
   - Price gauge (circular indicator)
   - Timeline for estimated holding period
   - Risk/reward chart
   - "Add to Portfolio" CTA button

INTERACTION STATES:
- Default: Subtle border, no glow
- Hover: Elevated shadow, neon glow, scale 1.02
- Active: Pressed state, scale 0.98
- Loading: Skeleton screens with shimmer effect
- Success: Green flash animation
- Error: Red shake animation

RESPONSIVE BEHAVIOR:
- Desktop (>1024px): 3-column bento grid
- Tablet (768-1024px): 2-column grid, collapsible sidebar
- Mobile (<768px): Single column, bottom navigation, swipe gestures

DARK MODE NATIVE:
- Pure black backgrounds
- High contrast text (WCAG AAA)
- Reduced motion option
- Glow effects more intense in dark

ACCESSIBILITY:
- Focus indicators with neon outline
- Keyboard navigation support
- Screen reader labels
- Color-blind friendly (not relying only on color)
- High contrast mode

MOOD/FEELING:
- Professional yet exciting
- Data-dense but not overwhelming
- Futuristic but trustworthy
- Fast and responsive
- Empowering and confident

AVOID:
- Cluttered layouts
- Too many colors
- Comic Sans or playful fonts
- Flat design (needs depth)
- Slow animations
- Skeuomorphism
```

---

## 🎨 PROMPTS ESPECÍFICOS POR COMPONENTE

### 1. Hero Card - Alpha Pick

```
Design a premium stock card for a financial terminal.

LAYOUT:
- Dark card with subtle gradient background
- Neon green accent border (2px, glowing)
- Rounded corners (12px)
- Padding: 32px

CONTENT HIERARCHY:
1. Badge "🏆 ALPHA PICK OF THE DAY" (top, small, gold)
2. Ticker "WEGE3" (large, 48px, bold, white)
3. Sector badge "Industrial" (pill shape, gray background)
4. Price comparison:
   - Current: R$ 45.80 (white, 24px)
   - Arrow →
   - Target: R$ 52.30 (green, 24px)
   - Label "Ceiling" (gray, 12px)
5. Progress bar showing 85% to ceiling (green fill, gray background)
6. Upside "+14.2%" (large, 32px, neon green, bold)
7. Time estimate "⏱️ 90 days" (gray, 14px)
8. Catalysts section:
   - Title "🚀 Catalysts" (16px, white)
   - Tags: "International expansion", "Tesla contract" (pills, dark bg, green border)
9. Metrics row:
   - "💡 Efficiency Score: 1.43"
   - "ROE: 22.3% | CAGR: 18.5% | P/L: 28.5"
10. Bottom row:
    - Badge "STRONG BUY" (green, bold, pulse animation)
    - Sentiment "😊 Normal" (gray)
11. CTA button "View Full Thesis →" (green border, hover glow)

EFFECTS:
- Hover: Card elevates, glow intensifies
- Numbers: Count-up animation on load
- Badge: Subtle pulse animation
```

### 2. Alerts Feed

```
Design a vertical feed of financial alerts.

CARD STRUCTURE:
- Compact height (80px)
- Dark background (#141419)
- Colored left border (4px, varies by type)
- Rounded corners (8px)
- Padding: 16px
- Margin between cards: 12px

ALERT TYPES:

GREEN (Buy Opportunity):
- Icon: 🟢 or ↓ arrow
- Border: Neon green
- Title: "OPPORTUNITY"
- Ticker: "ITUB4" (bold, 16px)
- Price: "R$ 28.90" (14px)
- Message: "Below ceiling (-8%)"
- Time: "2 hours ago" (gray, 12px)

RED (Take Profits):
- Icon: 🔴 or ↑ arrow
- Border: Electric red
- Title: "TAKE PROFITS"
- Ticker: "PETR4" (bold, 16px)
- Price: "R$ 38.50" (14px)
- Message: "Above ceiling (+12%)"
- Time: "5 hours ago" (gray, 12px)

YELLOW (Herd Risk):
- Icon: ⚠️
- Border: Gold yellow
- Title: "HERD RISK"
- Ticker: "MGLU3" (bold, 16px)
- Message: "Volume 3.2x above average"
- Time: "1 day ago" (gray, 12px)

ANIMATION:
- Slide in from right (300ms ease-out)
- Stagger delay (50ms between cards)
- New alert: Pulse effect
```

### 3. Elite Table

```
Design a modern data table for stock listings.

STRUCTURE:
- Dark background (#0a0a0f)
- Header row: Sticky, darker background (#141419)
- Rows: Alternating subtle backgrounds
- Grid lines: Very subtle (rgba(255,255,255,0.05))
- Rounded corners on container (12px)
- Padding: 16px

COLUMNS:
1. Rank (#) - 40px, centered, gray
2. Ticker - 80px, bold, white
3. Sector - 120px, badge with color
4. ROE - 80px, monospace, green if >20%
5. CAGR - 80px, monospace, green if >15%
6. P/L - 80px, monospace
7. Score - 80px, bold, gradient color
8. Upside - 100px, large, green, bold
9. Rec - 60px, emoji or badge
10. Chart - 120px, sparkline

HEADER:
- Text: 12px, uppercase, gray, bold
- Sort indicator: Arrow icon
- Hover: Lighter background

ROW:
- Height: 56px
- Default: Transparent
- Hover: Subtle glow, scale 1.01
- Click: Opens thesis panel

SECTOR BADGES:
- Pill shape, rounded
- Colors:
  - Financial: Blue
  - Energy: Orange
  - Tech: Purple
  - Industrial: Gray
  - Health: Green
  - Retail: Pink

SPARKLINE:
- Mini line chart (100x30px)
- Green line if trending up
- Red line if trending down
- Subtle gradient fill below line
```

### 4. Macro Bar

```
Design a horizontal status bar with macro indicators.

LAYOUT:
- Full width
- Height: 60px
- Dark background with subtle gradient
- Centered content
- Padding: 16px

INDICATORS (Horizontal layout):

1. Interest Rate:
   - Icon: 📈
   - Label: "Selic"
   - Value: "10.75%" (large, white)
   - Trend: ↑ (green) or ↓ (red)

2. Inflation:
   - Icon: 📊
   - Label: "IPCA"
   - Value: "4.5%" (large, white)
   - Trend: ↑ (red) or ↓ (green)

3. Favored Sectors:
   - Icon: ✅
   - Label: "Favored"
   - Values: "Financial, Energy, Health" (pills, green border)

SEPARATOR:
- Vertical line between indicators
- Subtle, 1px, rgba(255,255,255,0.1)

ANIMATION:
- Pulse on data update
- Smooth value transitions
```

### 5. Thesis Panel

```
Design a slide-out panel for detailed stock analysis.

DIMENSIONS:
- Width: 480px (desktop), 100% (mobile)
- Height: Full viewport
- Position: Fixed right
- Background: Dark (#0a0a0f) with slight transparency
- Backdrop blur: 10px

HEADER:
- Height: 80px
- Back button (←) on left
- Ticker in center (large, bold)
- Close button (×) on right
- Border bottom: Subtle line

CONTENT SECTIONS (Scrollable):

1. FUNDAMENTALS:
   - Title with icon
   - Metrics in grid (2 columns)
   - Each metric: Label + Value + Badge (Good/Fair/Poor)
   - Circular gauge for Efficiency Score

2. ENTRY STRATEGY:
   - Current price (large, white)
   - Ceiling price (green)
   - Ideal price (yellow)
   - Visual price ladder
   - Target profit (green, bold)
   - Stop loss (red)
   - Timeline bar (90 days)

3. CATALYSTS:
   - Numbered list
   - Each catalyst:
     - Icon (🚀, 📝, ⚡, 💡)
     - Title (bold)
     - Impact badge (High/Medium/Low)
     - Description (gray text)

4. MACRO CONTEXT:
   - Sector weight indicator
   - Interest rate impact
   - Inflation impact
   - Visual gauge for each

5. SENTIMENT:
   - Status badge (large)
   - Mention volume chart
   - Ratio indicator
   - Recommendation text

6. RISKS:
   - Warning icon
   - Bullet list
   - Red accent color

FOOTER:
- Sticky bottom
- CTA button "Add to Portfolio" (full width, green, bold)

ANIMATION:
- Slide in from right (400ms ease-out)
- Content fade in (stagger 50ms)
- Backdrop fade in
```

---

## 🎨 PALETA DE CORES COMPLETA

```css
/* Backgrounds */
--bg-primary: #0a0a0f;
--bg-secondary: #141419;
--bg-tertiary: #1a1a24;
--bg-card: rgba(20, 20, 25, 0.8);
--bg-hover: rgba(255, 255, 255, 0.05);

/* Accents */
--green-neon: #00ff88;
--green-dark: #00cc6a;
--green-light: #33ffaa;
--red-alert: #ff3366;
--red-dark: #cc2952;
--red-light: #ff5588;
--yellow-warning: #ffd700;
--yellow-dark: #ccaa00;
--blue-info: #00d4ff;
--blue-dark: #00a8cc;
--purple-tech: #a855f7;
--orange-energy: #fb923c;
--pink-retail: #ec4899;

/* Text */
--text-primary: #ffffff;
--text-secondary: #a0a0b0;
--text-muted: #606070;
--text-disabled: #404050;

/* Borders */
--border-subtle: rgba(255, 255, 255, 0.1);
--border-medium: rgba(255, 255, 255, 0.2);
--border-strong: rgba(255, 255, 255, 0.3);

/* Glows */
--glow-green: 0 0 20px rgba(0, 255, 136, 0.3);
--glow-red: 0 0 20px rgba(255, 51, 102, 0.3);
--glow-yellow: 0 0 20px rgba(255, 215, 0, 0.3);
--glow-white: 0 0 10px rgba(255, 255, 255, 0.2);

/* Gradients */
--gradient-bg: linear-gradient(135deg, #0a0a0f 0%, #0f0f1a 100%);
--gradient-card: linear-gradient(135deg, rgba(20,20,25,0.8) 0%, rgba(26,26,36,0.8) 100%);
--gradient-green: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
--gradient-red: linear-gradient(135deg, #ff3366 0%, #cc2952 100%);
```

---

## 📐 SPACING & SIZING

```css
/* Spacing Scale */
--space-xs: 4px;
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 32px;
--space-2xl: 48px;

/* Border Radius */
--radius-sm: 4px;
--radius-md: 8px;
--radius-lg: 12px;
--radius-xl: 16px;
--radius-full: 9999px;

/* Font Sizes */
--text-xs: 12px;
--text-sm: 14px;
--text-base: 16px;
--text-lg: 18px;
--text-xl: 20px;
--text-2xl: 24px;
--text-3xl: 32px;
--text-4xl: 48px;

/* Shadows */
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.5);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.5);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.5);
--shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.5);
```

---

## ✨ ANIMAÇÕES

```css
/* Transitions */
--transition-fast: 150ms ease-out;
--transition-base: 200ms ease-out;
--transition-slow: 300ms ease-out;

/* Keyframes */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes countUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes glow {
  0%, 100% { box-shadow: var(--glow-green); }
  50% { box-shadow: 0 0 30px rgba(0, 255, 136, 0.5); }
}
```

---

## 🎯 EXEMPLOS DE USO

### Para Midjourney:

```
/imagine a modern financial dashboard interface, dark theme with neon green accents, cyberpunk aesthetic, Bloomberg terminal style, bento grid layout, stock market data, clean typography, glassmorphism effects, professional UI design, 4k, high detail --ar 16:9 --v 6
```

### Para DALL-E:

```
Create a professional financial terminal dashboard with a dark cyberpunk aesthetic. The interface should feature a bento grid layout with a large hero card showing stock information, a sidebar with alerts, and a data table. Use neon green (#00ff88) and electric red (#ff3366) accents on a deep black background (#0a0a0f). Include glassmorphism effects, modern typography, and subtle glow effects. Style should be similar to Bloomberg Terminal meets Cyberpunk 2077 UI.
```

### Para Figma/Design Tools:

Use os componentes descritos acima como referência e aplique:
- Inter font family
- JetBrains Mono para números
- Paleta de cores fornecida
- Spacing scale consistente
- Efeitos de glow com box-shadow
- Animações suaves (200ms ease-out)

---

## 📱 RESPONSIVIDADE

### Desktop (>1024px)
- Bento grid: 3 colunas
- Hero card: 2 colunas
- Alerts: 1 coluna
- Table: Full width (3 colunas)
- Thesis panel: 480px slide-out

### Tablet (768-1024px)
- Bento grid: 2 colunas
- Hero card: 2 colunas
- Alerts: Collapsible accordion
- Table: Horizontal scroll
- Thesis panel: Full width overlay

### Mobile (<768px)
- Single column stack
- Hero card: Full width
- Alerts: Bottom sheet
- Table: Card view (vertical)
- Thesis panel: Full screen
- Bottom navigation bar

---

🎨 **Use este prompt para criar um design profissional e moderno que transmita confiança e tecnologia!**
