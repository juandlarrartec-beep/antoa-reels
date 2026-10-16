/* Guarda y devuelve el avance compartido de la hoja de ruta (solo estados, sin datos personales).
   Cada cambio se escribe como un archivo nuevo en Vercel Blob (hdr/estado-<marca de tiempo>.json);
   se lee el mas reciente y se borran los viejos. Al no reescribir nunca un archivo, la CDN no sirve datos viejos. */
const TAREAS = Array.from({ length: 18 }, (_, i) => 't' + String(i + 1).padStart(2, '0'));
const ESTADOS = ['pendiente', 'curso', 'espera', 'listo'];
const ENTREGAS = ['whatsapp', 'instagram', 'facebook', 'negocio', 'contenido', 'operativa', 'pauta'];
const CONSERVAR = 10;

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  try {
    const blob = global.__BLOB__ || (await import('@vercel/blob'));
    const q = req.query || {};
    const dueno = !!process.env.ADMIN_TOKEN && q.token === process.env.ADMIN_TOKEN;

    const { blobs } = await blob.list({ prefix: 'hdr/estado-' });
    const orden = blobs.slice().sort((a, b) => (a.pathname < b.pathname ? 1 : -1));
    let st = { tareas: {}, entregas: {}, actualizado: '' };
    if (orden[0]) {
      const r = await fetch(orden[0].url);
      if (r.ok) st = await r.json();
    }
    st.tareas = st.tareas || {};
    st.entregas = st.entregas || {};

    let escribir = false;
    let error = null;
    if (q.op === 'entrega') {
      if (ENTREGAS.includes(q.k) && (q.v === '1' || q.v === '0')) { st.entregas[q.k] = q.v === '1'; escribir = true; }
      else error = 'entrega invalida';
    } else if (q.op === 'tarea') {
      if (!dueno) error = 'sin permiso';
      else if (TAREAS.includes(q.id) && ESTADOS.includes(q.estado)) { st.tareas[q.id] = q.estado; escribir = true; }
      else error = 'tarea invalida';
    }

    if (escribir) {
      st.actualizado = new Date().toISOString();
      await blob.put('hdr/estado-' + Date.now() + '.json', JSON.stringify(st), {
        access: 'public', addRandomSuffix: false, contentType: 'application/json', cacheControlMaxAge: 60
      });
      const viejos = orden.slice(CONSERVAR - 1);
      if (viejos.length) await blob.del(viejos.map(b => b.url));
    }
    res.status(200).end(JSON.stringify({ ok: !error, error, owner: dueno, estado: st }));
  } catch (e) {
    res.status(500).end(JSON.stringify({ ok: false, error: 'servicio no disponible' }));
  }
};
