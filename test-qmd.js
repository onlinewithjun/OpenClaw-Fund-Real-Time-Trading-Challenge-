// Test if qmd.js can be imported
import('./qmd.js').then(module => {
    console.log('Module loaded successfully');
    console.log('Module exports:', Object.keys(module));
}).catch(err => {
    console.error('Error loading module:', err.message);
});