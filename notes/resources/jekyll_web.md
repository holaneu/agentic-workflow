Great to hear that the move to the `/docs` folder was successful! To change the **layout and design** of your Jekyll-based website, here’s a step-by-step guide on how to customize it effectively:

---

## **1. Understand Jekyll’s Structure**

In your `/docs` folder, Jekyll typically relies on:
- **Layouts:** Define the structure (`_layouts/`).
- **Includes:** Reusable snippets (`_includes/`).
- **Assets:** CSS, JS, images (`assets/`).
- **Config:** Site-wide settings (`_config.yml`).

If you don’t have these folders yet, you can create them.

---

## **2. Add a Custom Layout**

### **Folder Structure:**
```
/docs
├── _layouts/
│   └── default.html
├── _includes/
├── assets/
│   └── style.css
├── index.md
└── _config.yml
```

### **Example: `default.html`**

Create `/docs/_layouts/default.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{ page.title | default: site.title }}</title>
  <link rel="stylesheet" href="{{ '/assets/style.css' | relative_url }}">
</head>
<body>
  <header>
    <h1><a href="{{ '/' | relative_url }}">{{ site.title }}</a></h1>
    <nav>
      <a href="{{ '/' | relative_url }}">Home</a>
      <a href="{{ '/about' | relative_url }}">About</a>
    </nav>
  </header>

  <main>
    {{ content }}
  </main>

  <footer>
    <p>&copy; {{ site.time | date: '%Y' }} {{ site.title }}</p>
  </footer>
</body>
</html>
```

---

## **3. Apply the Layout to Your Pages**

In `index.md`:
```markdown
---
layout: default
title: Welcome to My Blog
---

# Hello, World!

This is my custom Jekyll website. Enjoy the new layout!
```

---

## **4. Add CSS Styling**

Create `/docs/assets/style.css`:
```css
body {
  font-family: Arial, sans-serif;
  background-color: #f9f9f9;
  color: #333;
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

header {
  background: #333;
  color: white;
  padding: 10px;
  text-align: center;
}

nav a {
  color: white;
  margin: 0 10px;
  text-decoration: none;
}

nav a:hover {
  text-decoration: underline;
}

footer {
  text-align: center;
  margin-top: 20px;
  font-size: 0.9em;
}
```

---

## **5. Update `_config.yml`**

Make sure your `_config.yml` in `/docs` includes:
```yaml
title: My Awesome Blog
theme: null  # Disable the default theme to use custom layouts
```

---

## **6. Commit & Push**

```bash
git add .
git commit -m "Add custom layout and styles"
git push
```

GitHub Pages will auto-deploy the changes.

---

## **Bonus: Advanced Customization Ideas**
- Add a **responsive design** using CSS Grid or Flexbox.
- Use `_includes/` for reusable components like headers or footers.
- Add **blog post listings** with Liquid:
  ```liquid
  {% for post in site.posts %}
    <h2><a href="{{ post.url }}">{{ post.title }}</a></h2>
    <p>{{ post.excerpt }}</p>
  {% endfor %}
  ```

Let me know if you need specific help with layouts, CSS, or Liquid templates!