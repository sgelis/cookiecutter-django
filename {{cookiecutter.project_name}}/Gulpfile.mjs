'use strict';


import gulp from 'gulp';
const { dest, parallel, series, src, watch } = gulp;

import browserify from 'browserify';
import { deleteAsync } from 'del';
import fancyLog from 'fancy-log';
import autoprefixer from 'gulp-autoprefixer';
import cleanCSS from 'gulp-clean-css';
import sass from 'gulp-dart-sass';
import uglify from 'gulp-uglify-es';
import tsify from 'tsify';
import source from 'vinyl-source-stream';
import watchify from 'watchify';


const paths = {
  styles: {
    scss: {
      src: [
        'src/**/*.scss',
        '!src/frontend/**/*.scss',
      ],
      dest: 'src/',
    },
    css: {
      src: [
        'src/**/*.css',
        '!src/frontend/**/*.css',
      ],
      dest: 'src/',
    },
  },
  scripts: {
    ts: {
      admin: {
        entryPoints: [
          'src/static/admin/js/main.ts',
        ],
        bundle: 'src/static/admin/js/',
      },
    },
    js: {
      src: [
        'src/**/*.js',
        '!src/frontend/**/*.js',
      ],
      dest: 'src/',
    },
  },
};

const watchedAdminBrowserify = watchify(
  browserify({
    basedir: '.',
    debug: true,
    entries: paths.scripts.ts.admin.entryPoints,
    cache: {},
    packageCache: {},
  }).plugin(tsify, { files: [] })
);


function compileSass() {
  return src(paths.styles.scss.src)
    .pipe(sass().on('error', sass.logError))
    .pipe(autoprefixer({ overrideBrowserslist: 'defaults' }))
    .pipe(dest(paths.styles.scss.dest));
}


function uglifyCSS() {
  return src(paths.styles.css.src)
    .pipe(cleanCSS({ inline: false }))
    .pipe(dest(paths.styles.css.dest))
}


function compileTSAdmin() {
  return browserify({
    basedir: '.',
    debug: true,
    entries: paths.scripts.ts.admin.entryPoints,
    cache: {},
    packageCache: {},
  })
    .plugin(tsify, { files: [] })
    .bundle()
    .pipe(source('bundle.js'))
    .pipe(dest(paths.scripts.ts.admin.bundle));
}


function watchTSAdmin() {
  return watchedAdminBrowserify
    .bundle()
    .on('error', fancyLog)
    .pipe(source('bundle.js'))
    .pipe(dest(paths.scripts.ts.admin.bundle));
}


function uglifyJS() {
  return src(paths.scripts.js.src)
    .pipe(uglify.default())
    .pipe(dest(paths.scripts.js.dest))
}


export function rmSrc() {
  return deleteAsync([
    "src/compiled_static/**/*.scss",
    "src/compiled_static/**/*.ts",
  ]);
}


watchedAdminBrowserify.on('update', watchTSAdmin);
watchedAdminBrowserify.on('log', fancyLog);


export const watchTS = watchTSAdmin;
export const watchSass = () => watch(paths.styles.scss.src, { ignoreInitial: false }, series(compileSass));
export const watchAll = parallel(watchTS, watchSass);
export const dev = watchAll;
export const buildTS = series(compileTSAdmin, uglifyJS);
export const buildSass = series(compileSass, uglifyCSS);
export const build = parallel(buildTS, buildSass);
export const buildDev = parallel(compileTSAdmin, compileSass);
export default build;
