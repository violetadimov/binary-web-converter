// =================== MONACO EDITOR SETUP ===================
console.log("generateOutput() was called");

//let htmlEditor, cssEditor, jsEditor, backendEditor;

require.config({ paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' } });

require(['vs/editor/editor.main'], function () {
  window.htmlEditor = monaco.editor.create(document.getElementById('htmlEditor'), {
    value: '',
    language: 'html',
    theme: 'vs-dark',
    automaticLayout: true
  });

  window.cssEditor = monaco.editor.create(document.getElementById('cssEditor'), {
    value: '',
    language: 'css',
    theme: 'vs-dark',
    automaticLayout: true
  });

  window.jsEditor = monaco.editor.create(document.getElementById('jsEditor'), {
    value: '',
    language: 'javascript',
    theme: 'vs-dark',
    automaticLayout: true
  });

  window.backendEditor = monaco.editor.create(document.getElementById('backendEditor'), {
    value: '',
    language: 'python',
    theme: 'vs-dark',
    automaticLayout: true
  });

  [htmlEditor, cssEditor, jsEditor].forEach(editor =>
    editor.onDidChangeModelContent(updatePreview)
  );

  updatePreview();
});

// =================== TOGGLE DEVICE VIEW ===================
function toggleDeviceView() {
  const preview = document.getElementById('livePreview');
  preview.classList.toggle('mobile-view');
  preview.classList.toggle('desktop-view');
}

// =================== LIVE PREVIEW ===================
function updatePreview() {
  if (!htmlEditor || !cssEditor || !jsEditor) return;

  const html = htmlEditor.getValue();
  const css = cssEditor.getValue();
  const js = jsEditor.getValue();

  const fullDoc = `
    <html>
      <head><style>${css}</style></head>
      <body>
        ${html}
        <script>${js}<\/script>
      </body>
    </html>`;

  const iframe = document.getElementById("livePreview");
  if (!iframe) return;
  const doc = iframe.contentDocument || iframe.contentWindow.document;
  doc.open();
  doc.write(fullDoc);
  doc.close();
}

// =================== SWITCH TABS ===================
function switchTab(tab) {
  const tabs = ['html', 'css', 'js', 'backend'];

  tabs.forEach(id => {
    document.getElementById(id + 'Editor').classList.add('hidden');
  });

  document.getElementById(tab + 'Editor').classList.remove('hidden');

  // Highlight active button
  const buttons = document.querySelectorAll('.tab-buttons button');
  buttons.forEach(btn => btn.classList.remove('active'));
  const activeBtn = Array.from(buttons).find(b => b.textContent.toLowerCase().includes(tab));
  if (activeBtn) activeBtn.classList.add('active');
}


// =================== SAVE PROJECT ===================
function saveProject() {
  const payload = {
    description: document.getElementById('commandInput')?.value || 'Untitled Project',
    html: htmlEditor.getValue(),
    css: cssEditor.getValue(),
    js: jsEditor.getValue(),
    backend: backendEditor.getValue(),
  };

  fetch("/save_project", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(data => alert(data.message || 'Project saved!'))
    .catch(err => alert('Save failed: ' + err.message));
}

// =================== GENERATE OUTPUT ===================
let contextPrompt = "";

function generateOutput() {
  const input = document.getElementById('commandInput').value.trim().toLowerCase();
  //const input = document.getElementById('commandInput').value.trim();
  if (!input) return;

  // Append to the full context prompt

  contextPrompt += "" + input.toLowerCase();
  document.getElementById('commandInput').value = "";

  let html = '', css = '', js = '', suggestions = [];

  // === Prompt Handlers ===
  if (contextPrompt.includes('e-commerce')) {
    html = `<header><h1>Welcome to My Store</h1><nav><a href="#">Home</a> | <a href="#">Shop</a></nav></header>
<main><div class="product"><h2>Product Name</h2><p>Description</p><button>Add to Cart</button></div></main>
<footer><p>&copy; 2025 My Store</p></footer>`;
    css = `body { font-family: sans-serif; margin: 0; }
header, footer { background: #111; color: white; text-align: center; padding: 1rem; }
main { padding: 1rem; }
.product { border: 1px solid #ccc; padding: 1rem; border-radius: 8px; }`;
    js = `document.querySelector("button").addEventListener("click", () => alert("Added to cart"));`;
    suggestions = ["Would you like to add a checkout page?", "Add a product search feature?"];
  }

  else if (contextPrompt.includes('portfolio')) {
    html = `<header><h1>Jane Doe – Portfolio</h1></header>
<section><h2>Projects</h2><ul><li>Project 1</li><li>Project 2</li></ul></section>
<footer>Contact: jane@example.com</footer>`;
    css = `body { font-family: Arial, sans-serif; }
header, footer { text-align: center; background: #eee; padding: 1rem; }
section { padding: 2rem; }`;
    suggestions = ["Embed a resume PDF", "Add a contact form or testimonials"];
  }

  else if (contextPrompt.includes('blog')) {
    html = `<header><h1>My Blog</h1></header>
    <article><h2>Post Title</h2><p>Content goes here...</p></article>`;
    css = `body { font-family: serif; margin: 0 auto; max-width: 600px; }
    header { background: #fafafa; padding: 1rem; text-align: center; }`;
    suggestions = ["Enable comments?", "Add categories or tags?"];
  }

  else if (contextPrompt.includes('landing page')) {
    html = `<section class="hero"><h1>Your Product</h1><p>Value proposition</p><button>Get Started</button></section>`;
    css = `.hero { background: #007bff; color: white; text-align: center; padding: 5rem; }`;
    suggestions = ["Add pricing section?", "Include testimonial carousel?"];
  }

  else {
    html = `<h1>Create7 is ready</h1><p>Your prompt was: "${input}"</p>`;
    css = `body { font-family: sans-serif; padding: 2rem; }`;
    suggestions = ["Try prompts like 'I want a blog', 'Build me a store', or 'Create a landing page'."];
  }

  htmlEditor.setValue(html);
  cssEditor.setValue(css);
  jsEditor.setValue(js);
  updatePreview();

  const suggestionBox = document.getElementById('suggestions');
  suggestionBox.innerHTML = suggestions.map(s => `<li class="suggestion-list" onclick="handleSuggestionClick('${s.replace(/'/g, "\\'")}')">${s}</li>`).join("");
}

function handleSuggestionClick(text) {
  const input = document.getElementById('commandInput');
  input.value = text;
  generateOutput();
}

function switchView(view) {
  const buttons = document.querySelectorAll('.tab-buttons button');
  const codeView = document.getElementById('codeView');
  const outputView = document.getElementById('outputView');
  buttons.forEach(btn => btn.classList.remove('active-active'));

  buttons.forEach(btn => btn.classList.remove('active'));
  document.querySelector(`[data-tab="${view}"]`).classList.add('active');

  if (view === 'code') {
    codeView.classList.remove('hidden');
    outputView.classList.add('hidden');
  } else {
    outputView.classList.remove('hidden');
    codeView.classList.add('hidden');
  }
}

function resetContext() {
  contextPrompt = "";
  alert("Context reset! You can start a new generation.")
  htmlEditor.setValue("");
  cssEditor.setValue("");
  jsEditor.setValue("");
  backendEditor.setValue("");
  document.getElementById("livePreview").srcdoc = "";
  document.getElementById("suggestions").innerHTML = "";
}