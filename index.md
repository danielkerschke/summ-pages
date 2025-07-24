Excellent! Let's build this from the ground up. I will give you the exact file names, where to create them in your project, and what code to put inside each one.

Prerequisite

You need a GitHub repository that is set up to be a GitHub Pages site. If you don't have one yet, you can follow the official GitHub guide to create one in just a few minutes. It's as simple as creating a repository and enabling Pages in the settings.

The Directory Structure

Your project folder (your repository) on your computer will look something like this. You will be creating the files and folders marked with <<--.

Generated code
your-repo-name/
├── _config.yml              (Jekyll configuration file, often created for you)
|
├── _includes/               <<-- CREATE THIS FOLDER
│   └── sidenote.html        <<-- CREATE THIS FILE
|
├── _layouts/                <<-- CREATE THIS FOLDER
│   └── default.html         <<-- CREATE THIS FILE
|
├── assets/                  <<-- CREATE THIS FOLDER
│   └── css/                 <<-- CREATE THIS FOLDER
│       └── style.scss       <<-- CREATE THIS FILE
|
└── index.md                 (Your main content page, usually created for you)

Step 1: The Sidenote "Lego Brick"

This is the reusable component for your notes.

Create the folder: In the root of your project, create a new folder named _includes.

Create the file: Inside the _includes folder, create a new file named sidenote.html.

Add the code: Copy and paste this code into _includes/sidenote.html.

Generated html
<aside class="sidenote">
  {{ include.text }}
</aside>
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Html
IGNORE_WHEN_COPYING_END

Purpose: This file defines the HTML structure for a single sidenote. {{ include.text }} is a placeholder that Jekyll will fill with your summary text.

Step 2: The Master Website Template

This is the main blueprint for every page on your site.

Create the folder: In the root of your project, create a new folder named _layouts.

Create the file: Inside the _layouts folder, create a new file named default.html.

Add the code: Copy and paste this code into _layouts/default.html.

Generated html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ page.title | default: site.title }}</title>
  <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
  <div class="page-wrapper">
    <header>
      <h1>My Awesome Website</h1>
    </header>

    <!-- The important wrapper for our layout -->
    <main class="content-with-sidenotes">
      {{ content }}
    </main>

    <footer>
      <p>© 2023 Your Name</p>
    </footer>
  </div>
</body>
</html>
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Html
IGNORE_WHEN_COPYING_END

Purpose: This file defines the overall HTML structure (header, footer, etc.). The most important part is <main class="content-with-sidenotes">, which wraps around your page's content ({{ content }}) and allows us to style it.

Step 3: The Styling (CSS)

This is what creates the two-column layout and makes it look good.

Create the folders: In the root of your project, create a folder named assets. Inside assets, create another folder named css.

Create the file: Inside the assets/css folder, create a new file named style.scss. (Note the .scss extension, which is important for Jekyll).

Add the code: Copy and paste this code into assets/css/style.scss.

Generated scss
---
---
// The two "---" lines above are required by Jekyll to process the file.

/* Basic body styling for readability */
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.6;
  color: #333;
  margin: 0;
  padding: 2rem;
}
.page-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

/* --- Sidenote Layout CSS --- */

// 1. Define the main content container with a grid layout.
.content-with-sidenotes {
  display: grid;
  // Creates columns: 200px for notes, a 40px gap, and the rest for content.
  grid-template-columns: 200px 1fr;
  grid-column-gap: 40px;
}

// 2. Style and position the sidenote itself.
.sidenote {
  grid-column: 1; // Put this in the first column.
  text-align: right;
  font-size: 0.9em;
  color: #666;
}

// 3. Place all main content (paragraphs, headings) in the second column.
.content-with-sidenotes > * {
  grid-column: 2;
}

// 4. ...BUT make sure our sidenotes go back into the first column!
// This overrides the rule above for our specific .sidenote class.
.content-with-sidenotes > .sidenote {
  grid-column: 1;
}

// 5. Responsive: For small screens, stack everything.
@media (max-width: 900px) {
  .content-with-sidenotes {
    display: block; // Go back to a normal, single-column flow.
  }

  .sidenote {
    // Style the note as an indented block above its paragraph on mobile.
    text-align: left;
    margin: 1em 0;
    padding: 1em;
    font-style: italic;
    background-color: #f8f8f8;
    border-left: 5px solid #ccc;
  }
}
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Scss
IGNORE_WHEN_COPYING_END

Purpose: This file tells the browser how to arrange the elements on the page. It creates the columns and handles the switch to a single-column view on mobile phones.

Step 4: Use Your New Feature!

Now you can use the sidenote in any Markdown page, like your index.md file.

Open your content file: Find the file named index.md in the root of your project.

Add the content: Replace whatever is in index.md with this example.

Generated markdown
---
layout: default
title: Home
---

## The Principle of Scannability

Good web design allows users to scan a page quickly to find what they're looking for. Long blocks of text can be intimidating. Marginalia, or sidenotes, help break up the text and provide quick summaries for the reader.
{% include sidenote.html text="Sidenotes make pages easy to scan." %}

This system works by using a Jekyll include. The include tag inserts a small piece of HTML into the final page. Our CSS then sees this new HTML element and uses a Grid layout to position it in the left-hand column, next to the paragraph it's associated with.
{% include sidenote.html text="It works using Jekyll and CSS Grid." %}

On mobile devices, a two-column layout doesn't work well. Our CSS includes a special rule called a media query. If the screen is too narrow, it automatically switches to a single-column layout and styles the sidenote as a simple, indented quote above the paragraph.
{% include sidenote.html text="The layout is fully responsive." %}
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Markdown
IGNORE_WHEN_COPYING_END

Purpose: This shows how you will actually write your content. The layout: default at the top tells Jekyll to use your master template. The {% include sidenote.html ... %} is your custom command to add a summary.

Final Step: Publish Your Site

Save all the files you've created.

Commit and push them to your GitHub repository using Git:

Generated bash
git add .
git commit -m "Implement sidenote feature"
git push
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

After a minute or two, GitHub will automatically build your site with the new files. Visit your GitHub Pages URL (your-username.github.io/your-repo-name/) and you will see your page with beautiful sidenotes
