/**
 * Highlight text utility functions
 */

/**
 * Highlight keywords in text
 * @param {string} text - Original text
 * @param {string[]} keywords - Keywords to highlight
 * @param {string} className - CSS class for highlight
 * @returns {string} HTML with highlighted text
 */
export function highlightText(text, keywords, className = 'highlight') {
  if (!text || !keywords || keywords.length === 0) {
    return text
  }

  let highlighted = text
  keywords.forEach((keyword) => {
    const regex = new RegExp(`(${escapeRegExp(keyword)})`, 'gi')
    highlighted = highlighted.replace(regex, `<span class="${className}">$1</span>`)
  })

  return highlighted
}

/**
 * Escape special regex characters
 * @param {string} string
 * @returns {string}
 */
function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

/**
 * Highlight code blocks in markdown
 * @param {string} markdown
 * @returns {string}
 */
export function highlightCodeBlocks(markdown) {
  // Simple code block highlighting
  return markdown
    .replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code class="language-$1">$2</code></pre>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
}

/**
 * Highlight diffs (additions and deletions)
 * @param {string} diffText
 * @returns {string}
 */
export function highlightDiff(diffText) {
  const lines = diffText.split('\n')
  return lines
    .map((line) => {
      if (line.startsWith('+')) {
        return `<span class="diff-add">${line}</span>`
      } else if (line.startsWith('-')) {
        return `<span class="diff-del">${line}</span>`
      }
      return line
    })
    .join('\n')
}
