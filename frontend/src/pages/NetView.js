import React, { useState, useEffect } from "react";
import Graph from "react-graph-vis";
import EventSideBar from "components/EventSideBar";
import { Button } from "reactstrap";
import Slider from "react-rangeslider";
import logoName from "../assests/imgs/IOTprint_wname.png";
import useWebSocket, { ReadyState } from "react-use-websocket";
import { DateTime } from "luxon";

const NetView = () => {
  const [data, setData] = useState(null);
  const [hostNodes, setHostNodes] = useState([]);
  const [hostEdges, setHostEdges] = useState([]);
  const [timestamp, setTimestamp] = useState(0);
  const [level, setLevel] = useState(1000);
  const [isLive, setIsLive] = useState(true);
  const historyTime = 30 * 60 * 1000; // 30min in millisec
  const { sendMessage, lastMessage, readyState } = useWebSocket(
    "ws://localhost:8000/netview-ws"
  );
  const options = {
    physics: {
      stabilization: false,
    },
    nodes: {
      color: "#53BF9D",
    },
    edges: {
      physics: false,
      color: "#233b91",
      arrows: {
        to: {
          enabled: true,
          type: "arrow",
        },

        from: {
          enabled: true,
          type: "arrow",
        },
      },
      length: 200,
    },
    height: "100%",
    width: "100%",
  };

  const events = {
    select: function (event) {
      var { nodes, edges } = event;
    },
  };

  const handleTimeStampChange = (value) => {
    setIsLive(false);
    setLevel(value);
  };

  useEffect(() => {
    if (lastMessage) setData(JSON.parse(lastMessage?.data));
  }, [lastMessage]);

  useEffect(() => {
    if (isLive && ReadyState.OPEN === readyState) sendMessage("latest");
  }, [isLive, readyState, sendMessage]);

  useEffect(() => {
    if (ReadyState.OPEN === readyState) sendMessage(timestamp);
  }, [timestamp]);

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
  const handleTimeStampFinishChange = (value) => {
    setTimestamp(new Date().getTime() - ((1000 - level) * historyTime) / 1000);
  };

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
        <div className="d-flex justify-content-between align-items-center">
          <Slider
            className="w-100"
            min={0}
            max={1000}
            tooltip={false}
            value={level}
            onChange={handleTimeStampChange}
            onChangeComplete={handleTimeStampFinishChange}
          />
          <Button
            style={{ width: "70px" }}
            className="d-flex align-items-center justify-content-around px-1 mx-1"
            onClick={(e) => {
              e.preventDefault();
              setIsLive(true);
              setLevel(1000);
            }}
            active={isLive}
            outline={isLive}
            color="primary"
          >
            <div
              style={{
                borderRadius: "50%",
                width: "10px",
                height: "10px",
                backgroundColor: "red",
              }}
            ></div>
            Live
          </Button>
          <img
            alt="logo-withname"
            src={logoName}
            style={{ width: "80px", float: "right" }}
          />
        </div>
        <p className="text-center">
          <b> Date:</b>
          {` ${DateTime.fromSeconds(timestamp / 1000).toLocaleString(
            DateTime.DATETIME_FULL_WITH_SECONDS
          )}`}
        </p>
      </div>
    </div>
  );
};

export default NetView;
