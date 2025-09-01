const path = require('path')

module.exports = {
  entry: './src/index.js',
  target: 'webworker',
  mode: 'production',
  optimization: {
    minimize: false
  },
  resolve: {
    extensions: ['.js', '.mjs'],
    fallback: {
      "crypto": false,
      "stream": false,
      "util": false,
      "buffer": false
    }
  },
  output: {
    filename: 'worker.js',
    path: path.resolve(__dirname, 'dist'),
    library: {
      type: 'module'
    }
  },
  experiments: {
    outputModule: true
  },
  externals: {
    '__STATIC_CONTENT_MANIFEST': '__STATIC_CONTENT_MANIFEST'
  }
}