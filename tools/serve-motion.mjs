import { parseArgs, checkOptions, numeric, previewAudio, startServer } from './motion-common.mjs';

const options = parseArgs(process.argv.slice(2));
checkOptions(options, ['help', 'silent', 'port', 'audio', 'audio-start', 'ffmpeg']);
if (options.help) {
  console.log('node tools/serve-motion.mjs [--port 5188] [--audio audio/current/song.mp3] [--audio-start 0] [--silent] [--ffmpeg PATH]');
} else {
  const audio = await previewAudio(options);
  try {
    const service = await startServer({ port: numeric(options.port, 5188, 'port', 0, 65535), audio: audio.path });
    console.log(`Six-world preview: ${service.url}`);
    console.log(audio.path ? `Audio: ${options.audio || 'audio/current/song.mp3'}; start ${options['audio-start'] || 0}s` : 'Audio pending or disabled: silent preview.');
    let stopping = false;
    async function stop() {
      if (stopping) return; stopping = true;
      await service.close(); await audio.cleanup();
    }
    process.once('SIGINT', stop); process.once('SIGTERM', stop);
  } catch (error) { await audio.cleanup(); throw error; }
}
