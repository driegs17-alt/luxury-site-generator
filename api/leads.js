module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    res.statusCode = 405;
    res.end("Method not allowed");
    return;
  }

  const body = req.body || {};
  const email = String(body.email || "").trim();
  const name = String(body.name || "").trim();

  if (!email || !email.includes("@") || email.length > 254) {
    res.statusCode = 400;
    res.end("Please enter a valid email.");
    return;
  }

  const lead = {
    email,
    name: name || null,
    source: body.source || "inquire",
    timestamp: new Date().toISOString(),
  };

  console.log("[lead]", JSON.stringify(lead));

  const webhook = process.env.LEADS_WEBHOOK_URL;
  if (webhook) {
    try {
      await fetch(webhook, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(lead),
      });
    } catch (err) {
      console.error("[lead webhook]", err);
    }
  }

  const wantsJson = String(req.headers.accept || "").includes("application/json");
  if (wantsJson) {
    res.statusCode = 200;
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.end(JSON.stringify({ ok: true }));
    return;
  }

  res.statusCode = 303;
  res.setHeader("Location", "/thank-you");
  res.end();
};