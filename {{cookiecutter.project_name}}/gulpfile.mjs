"use strict";


import browserify from "browserify";
import { deleteAsync } from "del";
import gulp from "gulp";
import autoprefixer from "gulp-autoprefixer";
import cleanCSS from "gulp-clean-css";
import sass from "gulp-dart-sass";
import ts from "gulp-typescript";
import uglify from "gulp-uglify-es";
import tsify from "tsify";
import source from "vinyl-source-stream";


const paths = {
    styles: {
        scss: {
            src: "src/**/*.scss",
            dest: "src/",
        },
        css: {
            src: "src/**/*.css",
            dest: "src/",
        },
    },
    scripts: {
        ts: {
            front: {
                entryPoints: [
                    "src/static/{{ cookiecutter.project_slug }}/js/main.ts",
                ],
                bundle: "src/static/{{ cookiecutter.project_slug }}/js/",
            },
            admin: {
                entryPoints: [
                    "src/static/admin/js/main.ts",
                ],
                bundle: "src/static/admin/js/",
            },
        },
        js: {
            src: "src/**/*.js",
            dest: "src/",
        },
    },
};


gulp.task("sass", function () {
    return gulp.src(paths.styles.scss.src)
        .pipe(sass().on("error", sass.logError))
        .pipe(autoprefixer({overrideBrowserslist: "defaults"}))
        .pipe(gulp.dest(paths.styles.scss.dest))
});

gulp.task("uglifyCSS", function () {
    return gulp.src(paths.styles.css.src)
        .pipe(cleanCSS({inline: false}))
        .pipe(gulp.dest(paths.styles.css.dest))
});

gulp.task("tsFront", function () {
    return browserify({
            basedir: ".",
            debug: true,
            entries: paths.scripts.ts.front.entryPoints,
            cache: {},
            packageCache: {},
        })
            .plugin(tsify)
            .bundle()
            .pipe(source("bundle.js"))
            .pipe(gulp.dest(paths.scripts.ts.front.bundle))
});

gulp.task("tsAdmin", function () {
    return browserify({
            basedir: ".",
            debug: true,
            entries: paths.scripts.ts.admin.entryPoints,
            cache: {},
            packageCache: {},
        })
            .plugin(tsify)
            .bundle()
            .pipe(source("bundle.js"))
            .pipe(gulp.dest(paths.scripts.ts.admin.bundle))
});

gulp.task("uglifyJs", function() {
    return gulp.src(paths.scripts.js.src)
        .pipe(uglify.default())
        .pipe(gulp.dest(paths.scripts.js.dest))
});

gulp.task("rmSrc", function () {
    return deleteAsync([
        "src/compiled_static/**/*.scss",
        "src/compiled_static/**/*.ts",
    ]);
});


gulp.task("fullSass", gulp.series("sass", "uglifyCSS", "rmSrc"));
gulp.task("ts", gulp.series("tsFront", "tsAdmin"));
gulp.task("fullTs", gulp.series("ts", "uglifyJs", "rmSrc"));
gulp.task("default", gulp.series("ts", "sass", "uglifyCSS", "uglifyJs", "rmSrc"));
