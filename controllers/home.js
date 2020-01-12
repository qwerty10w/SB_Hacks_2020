/**
 * GET /
 * Home page.
 */
exports.index = (req, res) => {
  console.log('home')
  res.render('home', {
    title: 'Home'
  });
};
