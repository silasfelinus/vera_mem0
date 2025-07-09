import eslintPluginPrettier from 'eslint-plugin-prettier'

export default [
  {
    ignores: ['.output', 'node_modules', '.nuxt'],
  },
  {
    files: ['**/*.{js,ts,vue}'],
    languageOptions: {
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
      },
    },
    plugins: {
      prettier: eslintPluginPrettier,
    },
    rules: {
      'prettier/prettier': 'error',
    },
  },
]
