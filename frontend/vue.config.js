const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  chainWebpack: (config) => {
    config.plugin('html').tap((args) => {
      args[0].title = 'Skågen Thought Validation'; 
      args[0].templateParameters = {
        BASE_URL: process.env.BASE_URL || '/' 
      };
      return args;
    });
  }
});

