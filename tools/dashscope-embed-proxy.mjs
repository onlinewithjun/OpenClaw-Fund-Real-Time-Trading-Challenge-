import http from 'node:http';

const PORT = Number(process.env.EMBED_PROXY_PORT || 18890);
const HOST = process.env.EMBED_PROXY_HOST || '127.0.0.1';
const TARGET = 'https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings';

const server = http.createServer(async (req, res) => {
  try {
    const url = req.url || '/';
    const isEmb = req.method === 'POST' && (url === '/embeddings' || url === '/v1/embeddings');
    const isHealth = req.method === 'GET' && (url === '/health' || url === '/v1/health');

    if (isHealth) {
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ ok: true, target: TARGET }));
      return;
    }

    if (!isEmb) {
      res.writeHead(404, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ error: 'not_found' }));
      return;
    }

    let body = '';
    req.on('data', (c) => {
      body += c;
      if (body.length > 2_000_000) req.destroy();
    });

    req.on('end', async () => {
      const auth = req.headers['authorization'] || '';
      const resp = await fetch(TARGET, {
        method: 'POST',
        headers: {
          'Authorization': auth,
          'Content-Type': 'application/json'
        },
        body
      });
      const text = await resp.text();
      res.writeHead(resp.status, { 'content-type': 'application/json' });
      res.end(text);
    });
  } catch (e) {
    res.writeHead(500, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ error: 'proxy_error', message: String(e?.message || e) }));
  }
});

server.listen(PORT, HOST, () => {
  console.log(`[embed-proxy] listening http://${HOST}:${PORT}`);
  console.log(`[embed-proxy] forwarding POST /v1/embeddings -> ${TARGET}`);
});
