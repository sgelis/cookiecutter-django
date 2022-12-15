import { bootstrapApplication } from "@angular/platform-browser";
import { provideRouter } from "@angular/router";

import { provideStore } from "@ngrx/store";
import { provideEffects } from "@ngrx/effects";
import { provideRouterStore } from "@ngrx/router-store";
import { provideStoreDevtools } from "@ngrx/store-devtools";

import { AppComponent } from "./app/app.component";
import { appRoutes } from "./app/app.routes";
import { appReducer } from "./app/store/app.reducer";
import { environment } from "./environments/environment";


bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(appRoutes),
    provideStore(appReducer),
    provideEffects(),
    provideRouterStore(),
    provideStoreDevtools({ logOnly: environment.production })
  ]
});
