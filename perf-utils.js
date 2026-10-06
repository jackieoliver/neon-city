/**
 * NEON CITY Performance Utilities
 * Shared code for optimizing experiences when embedded as iframes
 */

const NeonPerf = {
    // Detection
    isEmbedded: window.self !== window.top,
    isVisible: true,
    isPaused: false,

    // Settings (reduced for embedded mode)
    settings: {
        targetFPS: window.self !== window.top ? 30 : 60,
        particleMultiplier: window.self !== window.top ? 0.3 : 1.0,
        enableGlow: window.self === window.top,
        enableTrails: window.self === window.top,
        enableBloom: window.self === window.top,
        maxParticles: window.self !== window.top ? 200 : 2000,
    },

    // Frame rate limiting
    lastFrameTime: 0,
    frameInterval: 1000 / (window.self !== window.top ? 30 : 60),

    // Visibility handling
    init() {
        // Page Visibility API
        document.addEventListener('visibilitychange', () => {
            this.isVisible = !document.hidden;
            if (this.onVisibilityChange) {
                this.onVisibilityChange(this.isVisible);
            }
        });

        // Listen for pause messages from parent
        window.addEventListener('message', (e) => {
            if (e.data === 'neon-pause') {
                this.isPaused = true;
                if (this.onPause) this.onPause();
            } else if (e.data === 'neon-resume') {
                this.isPaused = false;
                if (this.onResume) this.onResume();
            }
        });

        // Notify parent we're ready
        if (this.isEmbedded) {
            window.parent.postMessage('neon-ready', '*');
        }

        console.log(`[NeonPerf] Embedded: ${this.isEmbedded}, Target FPS: ${this.settings.targetFPS}`);
    },

    // Throttled animation frame
    shouldRenderFrame(timestamp) {
        if (this.isPaused || !this.isVisible) {
            return false;
        }

        const elapsed = timestamp - this.lastFrameTime;
        if (elapsed < this.frameInterval) {
            return false;
        }

        this.lastFrameTime = timestamp - (elapsed % this.frameInterval);
        return true;
    },

    // Get adjusted particle count
    getParticleCount(baseCount) {
        return Math.min(
            Math.floor(baseCount * this.settings.particleMultiplier),
            this.settings.maxParticles
        );
    },

    // Callbacks
    onVisibilityChange: null,
    onPause: null,
    onResume: null
};

// Auto-init
NeonPerf.init();

// Make available globally
window.NeonPerf = NeonPerf;
