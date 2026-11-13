// Process-local compatibility adapter. No validation rule is changed, no dependency installed.
const Module = require('node:module');
const missing = '/Users/USER/.codex/skill-repos/FredTalk/apps/library/node_modules/typescript';
const existing = '/Users/USER/.npm/_npx/6286e9339036798b/node_modules/typescript';
const original = Module._resolveFilename;
Module._resolveFilename = function(request,parent,isMain,options){
 return original.call(this,request===missing?existing:request,parent,isMain,options);
};
