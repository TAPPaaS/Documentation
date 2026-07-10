import { defineConfig } from "astro/config";

// No `base`: the landing uses only relative links, and CI relativizes the
// generated asset URLs (see .woodpecker.yml build-landing) — one build works
// under any serving path.
export default defineConfig({});
