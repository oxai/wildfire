import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import { MapPage } from "./pages/MapPage";

export function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={MapPage} />
      </Switch>
    </Router>
  );
}
