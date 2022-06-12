import "bootstrap/dist/css/bootstrap.min.css";
import NetView from "pages/NetView";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import NavBar from "./components/NavBar";

function App() {
  return (
    <div className="App">
      <NavBar />
      <Router>
        <Switch>
          <Route exact path="/alerts/"></Route>
          <Route exact path="/">
            <NetView />
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
