/* TAPPaaS Custom JavaScript */

// Add any custom JavaScript functionality here

// Example: Smooth scroll for anchor links
document.addEventListener('DOMContentLoaded', function() {
  // Add smooth scrolling to all anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
});

// Example: Add copy button feedback
document.addEventListener('DOMContentLoaded', function() {
  const copyButtons = document.querySelectorAll('.md-clipboard');
  copyButtons.forEach(button => {
    button.addEventListener('click', function() {
      // Visual feedback is handled by MkDocs Material
      console.log('Code copied to clipboard');
    });
  });
});
