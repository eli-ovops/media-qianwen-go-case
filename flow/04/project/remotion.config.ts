import {Config} from '@remotion/cli/config';
// This task has a bounded dependency footprint. Avoid regenerable 300MB+ pack caches.
Config.overrideBundlerConfig((config) => ({...config, cache: false}));
// Also disable Remotion's separate cached-bundle store, not only webpack's pack cache.
Config.setCachingEnabled(false);
