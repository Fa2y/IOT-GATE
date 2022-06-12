import React from "react";
import logo from "../assests/imgs/IOTprint.png";
import {
  Navbar,
  NavbarBrand,
  NavbarToggler,
  Collapse,
  Nav,
  NavItem,
  NavLink,
} from "reactstrap";

const NavBar = () => {
  return (
    <Navbar color="light" expand="md" light>
      <NavbarBrand href="/">
        <img src={logo} style={{ width: "50px" }} alt="LOGO" />
        <b className="mx-3" style={{ color: "#233b91" }}>
          IOTGate
        </b>
      </NavbarBrand>
      <NavbarToggler onClick={function noRefCheck() {}} />
      <Collapse navbar>
        <Nav className="me-auto" navbar>
          <NavItem>
            <NavLink href="/alerts/">Alerts</NavLink>
          </NavItem>
          <NavItem>
            <NavLink href="/">NetView</NavLink>
          </NavItem>
        </Nav>
      </Collapse>
    </Navbar>
  );
};

export default NavBar;
