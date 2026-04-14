from gevent import monkey
monkey.patch_all()

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

latest_command = "S"

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
  <title>RC Car Remote</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: #0d0d0d;
      color: #e0e0e0;
      font-family: 'Segoe UI', system-ui, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 12px;
      padding: 20px;
      touch-action: manipulation;
      user-select: none;
    }

    h1 {
      font-size: 1.3rem;
      font-weight: 600;
      letter-spacing: 0.06em;
      color: #a0c4ff;
      text-transform: uppercase;
    }

    #status-bar {
      font-size: 0.85rem;
      color: #888;
      height: 20px;
    }

    #status-bar span {
      color: #64ffda;
      font-weight: 600;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(3, 90px);
      grid-template-rows: repeat(3, 90px);
      gap: 12px;
    }

    .btn {
      background: #1a1a2e;
      border: 2px solid #2a2a4a;
      border-radius: 16px;
      color: #c0c8ff;
      font-size: 2rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.1s, border-color 0.1s, transform 0.1s;
      -webkit-tap-highlight-color: transparent;
    }

    .btn:active,
    .btn.active {
      background: #2a2a6e;
      border-color: #6080ff;
      transform: scale(0.94);
      color: #ffffff;
    }

    .btn.stop {
      background: #2a0a0a;
      border-color: #6a1a1a;
      color: #ff6060;
    }

    .btn.stop.active {
      background: #5a1010;
      border-color: #ff4040;
    }

    .btn-forward  { grid-column: 2; grid-row: 1; }
    .btn-left     { grid-column: 1; grid-row: 2; }
    .btn-stop     { grid-column: 2; grid-row: 2; }
    .btn-right    { grid-column: 3; grid-row: 2; }
    .btn-backward { grid-column: 2; grid-row: 3; }

    .label-row {
      display: flex;
      gap: 16px;
      font-size: 0.75rem;
      color: #555;
      letter-spacing: 0.04em;
    }
  </style>
</head>
<body>
  <h1>&#9654; RC Car Remote</h1>
  <div id="status-bar">Command: <span id="cmd-label">S</span></div>

  <div class="grid">
    <button class="btn btn-forward"   id="btn-F" data-cmd="F">&#9650;</button>
    <button class="btn btn-left"      id="btn-L" data-cmd="L">&#9664;</button>
    <button class="btn btn-stop stop" id="btn-S" data-cmd="S">&#9632;</button>
    <button class="btn btn-right"     id="btn-R" data-cmd="R">&#9654;</button>
    <button class="btn btn-backward"  id="btn-B" data-cmd="B">&#9660;</button>
  </div>

  <div class="label-row">
    <span>FORWARD</span><span>BACKWARD</span><span>LEFT</span><span>RIGHT</span><span>STOP</span>
  </div>

  <script>
    async function sendCmd(cmd) {
      document.getElementById('cmd-label').textContent = cmd;
      try {
        await fetch('/update', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ command: cmd })
        });
      } catch (e) { console.warn('send failed', e); }
    }

    document.querySelectorAll('.btn').forEach(btn => {
      const cmd = btn.dataset.cmd;

      const press = (e) => {
        e.preventDefault();
        btn.classList.add('active');
        sendCmd(cmd);
      };

      const release = (e) => {
        e.preventDefault();
        btn.classList.remove('active');
        if (cmd !== 'S') sendCmd('S');
      };

      btn.addEventListener('mousedown',   press);
      btn.addEventListener('mouseup',     release);
      btn.addEventListener('mouseleave',  release);
      btn.addEventListener('touchstart',  press,   { passive: false });
      btn.addEventListener('touchend',    release, { passive: false });
      btn.addEventListener('touchcancel', release, { passive: false });
    });
  </script>
</body>
</html>"""


@app.route('/')
def index():
    return render_template_string(HTML_PAGE)


@app.route('/update', methods=['POST'])
def update():
    global latest_command
    data = request.get_json(silent=True) or {}
    cmd = data.get('command', 'S').upper().strip()
    if cmd in ('F', 'B', 'L', 'R', 'S'):
        latest_command = cmd
    return jsonify({"status": "ok", "command": latest_command})


@app.route('/command', methods=['GET'])
def command():
    return latest_command, 200, {'Content-Type': 'text/plain'}


if __name__ == '__main__':
    app.run(debug=False)