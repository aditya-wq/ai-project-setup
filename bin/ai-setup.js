#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

// ─── STYLING ─────────────────────────────────────────────────────────────────
const c = {
  reset: "\x1b[0m",
  green: "\x1b[32m",
  cyan: "\x1b[36m",
  yellow: "\x1b[33m",
  red: "\x1b[31m",
  bold: "\x1b[1m",
  dim: "\x1b[2m",
  magenta: "\x1b[35m",
};

const log = {
  info: (msg) => console.log(`${c.cyan}[INFO]${c.reset} ${msg}`),
  ok: (msg) => console.log(`${c.green}[OK]${c.reset} ${msg}`),
  warn: (msg) => console.log(`${c.yellow}[WARN]${c.reset} ${msg}`),
  err: (msg) => console.log(`${c.red}[ERROR]${c.reset} ${msg}`),
  title: (msg) => console.log(`\n${c.bold}${c.cyan}--- ${msg} ---${c.reset}`),
  status: (msg) => console.log(`${c.magenta}✨${c.reset} ${msg}`),
};

// ─── DISCOVERY ENGINE ────────────────────────────────────────────────────────
function discoverProject(targetDir) {
  const files = fs.readdirSync(targetDir);
  const stack = [];
  const indicators = {
    "package.json": "Node.js",
    "requirements.txt": "Python",
    "pyproject.toml": "Python (Poetry/Modern)",
    "go.mod": "Go",
    "pom.xml": "Java (Maven)",
    "build.gradle": "Java (Gradle)",
    "Cargo.toml": "Rust",
    "composer.json": "PHP",
    "Gemfile": "Ruby",
    "CMakeLists.txt": "C/C++",
    "Makefile": "Build-based System",
    "docker-compose.yml": "Dockerized Environment",
    ".vercel": "Vercel Deployment",
    "tailwind.config.js": "Tailwind CSS",
    "next.config.js": "Next.js",
  };

  for (const [file, name] of Object.entries(indicators)) {
    if (files.includes(file) || files.some(f => f.startsWith(file))) {
      stack.push(name);
    }
  }

  if (files.includes("package.json")) {
    try {
      const pkg = JSON.parse(fs.readFileSync(path.join(targetDir, "package.json"), "utf8"));
      const deps = { ...pkg.dependencies, ...pkg.devDependencies };
      if (deps["next"]) stack.push("Next.js App Router");
      if (deps["react"]) stack.push("React");
      if (deps["vue"]) stack.push("Vue.js");
      if (deps["express"]) stack.push("Express.js");
      if (deps["@nestjs/core"]) stack.push("NestJS");
      if (deps["typescript"]) stack.push("TypeScript (Strict)");
      if (deps["prisma"] || deps["@prisma/client"]) stack.push("Prisma ORM");
      if (deps["drizzle-orm"]) stack.push("Drizzle ORM");
      if (deps["tailwindcss"]) stack.push("Tailwind CSS");
    } catch (e) {}
  }

  return stack.length > 0 ? stack : ["Unidentified Technical Stack"];
}

// ─── CONTENT GENERATOR ───────────────────────────────────────────────────────
function generateContent(stack) {
  const stackList = stack.map(s => `- ${s}`).join("\n");

  return `# AI Master Brain — Delivery Excellence Protocol

> **CRITICAL**: Every AI agent reading this file must comply with all rules below without exception.
> This is the singular source of truth for this project. Follow it before applying any personal defaults.

---

## Project DNA
- **Detected Stack**:
${stackList}
- **Delivery Standard**: Premium Production-Grade (Zero Tolerance for Incomplete Output)

---

## SECTION 1 — WHAT YOU MUST NEVER DO

These are absolute prohibitions. Violating any of these is a failed deliverable.

1. **No dead buttons.** Every button must have a real, working event handler. No \`onClick={() => {}}\`, no \`// TODO\`, no console.log only. If a button cannot work yet, do not render it.
2. **No demo or placeholder data in final output.** Build real state management: loading state → data state → error state → empty state. Never hardcode fake data as final output.
3. **No half-built features.** If you start implementing a feature (modal, form, slider, nav), you must complete it 100% — open, interaction, close, edge cases — before moving to the next.
4. **No layouts that only work on one screen size.** Every UI element must be verified at 375px, 768px, 1280px, and 1920px. No horizontal scroll. No overflowing content.
5. **No generic or cookie-cutter designs.** Plain white background with a flat blue button is rejected. Every design must feel premium, intentional, and crafted.
6. **No missing dependencies.** Every library you use must include an explicit install command. Never assume a library is installed.
7. **No broken imports.** Every import at the top of a file must exist and be installed.
8. **No broken navigation.** Hamburger menus must open AND close properly. Every link must navigate to a real route.
9. **No forms without full handling.** Every form requires: client-side validation, loading state on submit, success state, error state.
10. **No code you have not mentally traced.** Read your own function as if you are the runtime. Verify the logic path before writing it.

---

## SECTION 2 — MANDATORY DELIVERY CHECKLIST

Run through this list before submitting ANY component or feature:

### Functionality
- Every button has a real, tested handler
- Every form validates and handles all three states: loading, success, error
- All API calls use loading/success/error state management
- Navigation works at all screen sizes including mobile hamburger
- Modals, drawers, dropdowns all open AND close correctly
- All interactive elements have hover, focus, and active visual states
- All dynamic content actually fetches and renders

### Responsiveness
- Verified at 375px — no horizontal scroll, no broken stacking
- Verified at 768px — tablet columns and nav correct
- Verified at 1280px — desktop layout renders as designed
- Images are contained and never overflow
- Touch targets are minimum 44×44px on mobile

### Design
- Color palette is consistent and curated — no accidental color mixing
- Font system uses one typeface with a clear scale
- Spacing follows the 4px grid system (4, 8, 12, 16, 24, 32, 48, 64px)
- Dark mode OR light mode is consistently applied throughout
- All interactive elements have smooth 150-200ms transitions
- No element looks like a default browser style

### Code Health
- All dependencies are listed with install commands
- No unused imports
- No TypeScript \`any\` types
- No hardcoded API keys, secrets, or tokens

---

## SECTION 3 — PREMIUM DESIGN PROTOCOL

### Color System
- Use HSL for precise palette control
- Dark surface stack: \`hsl(230, 15%, 6%)\` → \`hsl(230, 12%, 12%)\` → \`hsl(230, 10%, 18%)\`
- Accent: define primary, hover (+8% lightness), active (-5% lightness)
- Text: use \`hsl(230, 20%, 92%)\` for primary and \`hsl(230, 10%, 60%)\` for secondary
- Never use flat black (\`#000000\`) or flat white (\`#ffffff\`) as primary surfaces

### Typography
- Import from Google Fonts: Inter, Outfit, or Geist Sans (pick one per project)
- Scale: 12 / 14 / 16 / 20 / 24 / 32 / 48 / 64px
- Line height: body = 1.6, headings = 1.15
- Letter spacing: headings = -0.025em
- Never use the browser default system font stack

### Motion
- Hover transitions: 150ms ease-in-out on all interactive elements
- Page transitions: 200ms opacity fade
- Loading states: animated skeletons — not raw spinners on blank pages
- Micro-interactions: subtle transform scale(1.02) and brightness shift on hover

### Layout
- CSS Grid for two-dimensional page structure
- Flexbox for one-dimensional component alignment
- Mobile-first: build 375px baseline, use \`min-width\` media queries to scale up
- Max content width: 1280px, centered with responsive horizontal padding

---

## SECTION 4 — COMPONENT STANDARDS

### Header / Navigation
- Logo: renders correctly at all sizes
- Desktop nav: all links functional and styled
- Mobile nav: hamburger icon visible below 768px, menu opens full-width overlay, all links navigate, menu closes on link click and on outside click
- Active route is visually distinguished
- Sticky or fixed behavior implemented and tested (does not cover content)

### Footer
- All links are functional (no href="#" placeholders)
- Social icons linked to real URLs or clearly marked as placeholder
- Copyright year rendered correctly
- Fully responsive — stacks to single column on mobile

### Sliders / Carousels
- Previous and Next controls work
- Auto-play works and pauses on user hover/focus
- Dot indicators update to reflect current slide
- Touch swipe works on mobile
- Does not cause layout shift on load

### Forms
- Input labels are semantically linked (\`for\`/\`id\` pairing)
- Required fields validated before submission fires
- Button shows loading spinner during async request
- Success feedback rendered inline or as a toast
- Error message is clearly visible and dismissible
- Form is reset or redirected after successful submission

### Modals / Drawers
- Open trigger (button) works
- X button closes it
- Clicking the backdrop closes it
- Pressing Escape closes it
- Body scroll is locked while modal is open
- Content is scrollable if it overflows the modal height

---

## SECTION 5 — DEPENDENCY PROTOCOL

Every time you introduce a new library, you must:

1. State the purpose: "Installing X to handle Y."
2. Provide the exact command:
\`\`\`bash
npm install <package-name>
# or for dev-only
npm install -D <package-name>
\`\`\`
3. Import it correctly at the top of every file that uses it.
4. Never reference a library that has not been installed.

---

## SECTION 6 — ENGINEERING STANDARDS

### TypeScript
- Strict mode always enabled
- No \`any\` types — use \`unknown\` and narrow it
- Interfaces for object shapes, types for unions and aliases

### Security
- All environment secrets in \`.env\` files only
- Never log tokens, passwords, or PII
- Validate all external input (API bodies, URL params, user input) at the boundary

### API Design
- Authenticate before any logic runs
- Validate with Zod schema before touching the database
- Return proper HTTP codes: 200, 201, 400, 401, 403, 404, 500
- Error shape: \`{ error: string, code?: string }\`

### Database
- SELECT only the columns you need — never \`SELECT *\`
- Use transactions for multi-table writes
- Never string-interpolate SQL — use parameterized queries or ORM

---

## SECTION 7 — QUALITY GATE

Before any deliverable is considered complete, it must pass ALL of these:

- A senior designer would be proud of this UI
- Every button works when a real user clicks it
- The layout is correct on a 375px iPhone screen
- All dependencies are installed and imported
- No feature is left half-built
- No placeholder or "TODO" exists in delivered code

---

## SECTION 8 — EFFICIENCY PROTOCOL (ALWAYS ON)

You are operating in **Maximum Efficiency Mode**. These rules override all default verbosity. Active every response. No drift. No revert.

### Response Rules
- **Answer only what was asked.** No preamble, no recap, no "Great question!", no closing remarks.
- **No explanations unless asked.** If the user asks "fix this", fix it. Do not explain what was wrong unless they ask "why".
- **No summaries after code.** Code speaks. Do not re-describe what the code does in prose after writing it.
- **No listing what you're about to do.** Just do it.
- **No "I've updated X to do Y" commentary.** Show the result.

### Code Rules
- **Always output full, working code.** Never truncate. Never use \`// ... rest of code\`. Never use \`// existing code here\`.
- **Never break functions.** All function signatures, logic, and return values must be preserved unless explicitly told to change them.
- **No placeholder implementations.** No \`TODO\`, no \`throw new Error("not implemented")\`, no stub bodies.
- **Code output is never compressed.** Prose is terse. Code is complete.

### Trigger / Reset
- **On**: Default. Active from first message every session.
- **Off**: User says "explain this" or "walk me through it" — then explain, then return to efficiency mode.

---

## Project Memory
<!-- AI agents: update this section as the project evolves to save context tokens -->
- **Session Focus**: [Active development target]
- **Key Decisions**: [Record major architectural choices here]
- **Completed**: [Features that are done and working]
- **In Progress**: [Features currently being built]
- **Pending**: [Features not yet started]
`;
}

// ─── MAIN ────────────────────────────────────────────────────────────────────

function main() {
  const args = process.argv.slice(2);
  const force = args.includes("--force") || args.includes("-f");
  const targetDir = args.find((a) => !a.startsWith("-")) || process.cwd();

  console.log("\n" + c.bold + c.cyan + "+------------------------------------------+" + c.reset);
  console.log(c.bold + c.cyan + "|    Universal AI Setup v3.1 — Delivery    |" + c.reset);
  console.log(c.bold + c.cyan + "|         Excellence Protocol              |" + c.reset);
  console.log(c.bold + c.cyan + "+------------------------------------------+" + c.reset);
  console.log(c.dim + "Target: " + path.resolve(targetDir) + c.reset + "\n");

  if (!fs.existsSync(path.resolve(targetDir))) {
    fs.mkdirSync(path.resolve(targetDir), { recursive: true });
  }
  process.chdir(path.resolve(targetDir));

  // -- 1. Cleanup legacy configuration
  log.title("Cleaning legacy artifacts");
  const legacyItems = [
    ".ai", ".claude", ".cursorrules", ".windsurfrules", "AI.md", "CLAUDE.md",
    "ANTIGRAVITY.md", "COEXISTENCE.md", ".github/copilot-instructions.md"
  ];

  legacyItems.forEach(item => {
    const fullPath = path.resolve(item);
    if (fs.existsSync(fullPath)) {
      if (fs.lstatSync(fullPath).isDirectory()) {
        fs.rmSync(fullPath, { recursive: true, force: true });
      } else {
        fs.unlinkSync(fullPath);
      }
      log.info(`Purged: ${item}`);
    }
  });

  // -- 2. Discovery
  log.title("Analyzing project DNA");
  const stack = discoverProject(process.cwd());
  log.status(`Detected: ${stack.join(", ")}`);

  // -- 3. Generate unified .ai file
  log.title("Generating Delivery Excellence Brain (.ai)");
  const aiFilePath = path.join(process.cwd(), ".ai");
  if (!force && fs.existsSync(aiFilePath)) {
    log.warn("File .ai already exists. Use --force to overwrite.");
  } else {
    fs.writeFileSync(aiFilePath, generateContent(stack), "utf8");
    log.ok("Synchronized .ai — Delivery Excellence Protocol active");
  }

  // -- Summary
  console.log("\n" + c.bold + "--------------------------------------------------" + c.reset);
  console.log(c.green + c.bold + "Setup Complete — Delivery Excellence Active" + c.reset);
  console.log("Singular intelligence established in: " + c.cyan + ".ai" + c.reset);
  console.log("\n" + c.bold + "Usage:" + c.reset);
  console.log("  1. Reference " + c.cyan + ".ai" + c.reset + " at the start of every AI session (e.g., @.ai in Cursor)");
  console.log("  2. The agent is now bound to production-quality delivery standards");
  console.log("  3. Run " + c.cyan + "ai --force" + c.reset + " to re-scan and update after stack changes\n");
}

main();
