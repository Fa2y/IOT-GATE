import EventSideBar from "components/EventSideBar";
import React, { useState, useEffect } from "react";
import Graph from "react-graph-vis";
import logoName from "../assests/imgs/IOTprint_wname.png";

const NetView = () => {
  const [data, setData] = useState(null);
  const [hostNodes, setHostNodes] = useState([]);
  const [hostEdges, setHostEdges] = useState([]);
  // const graph = {
  //   nodes: [
  //     { id: 1, label: "Node 1", title: "node 1 tootip text" },
  //     { id: 2, label: "Node 2", title: "node 2 tootip text" },
  //     { id: 3, label: "Node 3", title: "node 3 tootip text" },
  //     { id: 4, label: "Node 4", title: "node 4 tootip text" },
  //     { id: 5, label: "Node 5", title: "node 5 tootip text" },
  //   ],
  //   edges: [
  //     { from: 1, to: 2 },
  //     { from: 1, to: 3 },
  //     { from: 2, to: 4 },
  //     { from: 2, to: 5 },
  //   ],
  // };

  const options = {
    // layout: {
    //   hierarchical: true,
    // },
    nodes: {
      color: "#53BF9D",
    },
    edges: {
      color: "#233b91",
    },
    height: "100%",
    width: "100%",
  };

  const events = {
    select: function (event) {
      var { nodes, edges } = event;
    },
  };

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/hosts-ws");
    ws.onmessage = (event) => {
      setData(JSON.parse(event?.data));
    };
  }, []);

  useEffect(() => {
    if (data) {
      if (data?.hosts?.length > 0) {
        setHostNodes(
          data?.hosts?.map((host, index) => ({
            id: index,
            label: host,
            title: "HELLOWORLD",
          }))
        );
      }
      if (data?.connections?.length > 0) {
        setHostEdges(
          data?.connections?.map((edge) => ({
            from: data?.hosts?.indexOf(edge?.split("-")[0]),
            to: data?.hosts?.indexOf(edge?.split("-")[1]),
          }))
        );
      }
    }
  }, [data]);

  return (
    <div className="d-flex ">
      <EventSideBar />
      <div>
        <Graph
          style={{
            height: "600px",
            borderRadius: "10px",
            borderStyle: "solid",
            borderColor: "#233b91",
          }}
          graph={{ nodes: hostNodes, edges: hostEdges }}
          options={options}
          events={events}
          // getNetwork={(network) => {
          //   //  if you want access to vis.js network api you can set the state in a parent component using this property
          // }}
        />
        <img
          alt="logo-withname"
          src={logoName}
          style={{ width: "80px", float: "right" }}
        />
      </div>
    </div>
  );
};

export default NetView;
