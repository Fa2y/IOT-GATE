import "bootstrap/dist/css/bootstrap.min.css";
import NetView from "pages/NetView";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import NavBar from "./components/NavBar";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

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
      <ToastContainer
        position="top-center"
        autoClose={5000}
        style={{ width: "50%" }}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        theme="colored"
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
    </div>
  );
}

export default App;
