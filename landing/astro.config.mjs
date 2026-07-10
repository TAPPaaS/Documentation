import { defineConfig } from "astro/config";

// The landing is served under a sub-path on Codeberg Pages
// (e.g. /Documentation/@pages-spike-b/); CI injects it via ASTRO_BASE.
// Locally (`npm run dev`) it defaults to /.
export default defineConfig({
  base: process.env.ASTRO_BASE || "/",
});
