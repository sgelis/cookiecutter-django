"use strict";


import browserify from "browserify";
import { deleteAsync } from "del";
import fancyLog from "fancy-log";
import gulp from "gulp";
import autoprefixer from "gulp-autoprefixer";
import cleanCSS from "gulp-clean-css";
import sass from "gulp-dart-sass";
import ts from "gulp-typescript";
import uglify from "gulp-uglify-es";
import tsify from "tsify";
import source from "vinyl-source-stream";
import watchify from "watchify";


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

const watchedFrontBrowserify = watchify(
    browserify({
        basedir: ".",
        debug: true,
        entries: paths.scripts.ts.front.entryPoints,
        cache: {},
        packageCache: {},
    }).plugin(tsify)
);
const watchedAdminBrowserify = watchify(
    browserify({
        basedir: ".",
        debug: true,
        entries: paths.scripts.ts.admin.entryPoints,
        cache: {},
        packageCache: {},
    }).plugin(tsify)
);


gulp.task("sass", function () {
    return gulp.src(paths.styles.scss.src)
        .pipe(sass().on("error", sass.logError))
        .pipe(autoprefixer({overrideBrowserslist: "defaults"}))
        .pipe(gulp.dest(paths.styles.scss.dest))
});

gulp.task("uglify:css", function () {
    return gulp.src(paths.styles.css.src)
        .pipe(cleanCSS({inline: false}))
        .pipe(gulp.dest(paths.styles.css.dest))
});

gulp.task("ts:front", function () {
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

gulp.task("ts:admin", function () {
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

function watchTsFront () {
    return watchedFrontBrowserify
        .bundle()
        .on("error", fancyLog)
        .pipe(source("bundle.js"))
        .pipe(gulp.dest(paths.scripts.ts.front.bundle))
}

function watchTsAdmin () {
    return watchedAdminBrowserify
        .bundle()
        .on("error", fancyLog)
        .pipe(source("bundle.js"))
        .pipe(gulp.dest(paths.scripts.ts.admin.bundle))
}

gulp.task("uglify:js", function() {
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


gulp.task("watch:ts", gulp.parallel(watchTsFront, watchTsAdmin));
gulp.task("watch:sass", function () {
    return gulp.watch(paths.styles.scss.src, {ignoreInitial: false}, gulp.series("sass"))
});
gulp.task("watch", gulp.parallel("watch:ts", "watch:sass"));
gulp.task("dev", gulp.series("watch"));
gulp.task("build:ts", gulp.series(gulp.parallel("ts:front", "ts:admin"), "uglify:js"));
gulp.task("build:sass", gulp.series("sass", "uglify:css"));
gulp.task("build", gulp.parallel("build:ts", "build:sass"));
gulp.task("default", gulp.series("build"));

watchedFrontBrowserify.on("update", watchTsFront)
watchedFrontBrowserify.on("log", fancyLog)
watchedAdminBrowserify.on("update", watchTsAdmin)
watchedAdminBrowserify.on("log", fancyLog)
