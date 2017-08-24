import _ from 'lodash';
import exact from 'prop-types-exact';
import propTypes from 'prop-types';
import withScriptjs from 'react-google-maps/lib/async/withScriptjs';
import { GoogleMap as GMap, withGoogleMap } from 'react-google-maps';
import React, { Component } from 'react';

const apiKey = 'AIzaSyAIXwxQFZ9j3VPmvSZ4ip0tqeT9YxmWxAc';

const AsyncMap = _.flowRight(
    withScriptjs,
    withGoogleMap,
    )(props => (
        <GMap
            defaultCenter={props.defaultCenter}
            defaultZoom={props.defaultZoom}
            onClick={props.onClick}
            ref={props.onMapLoad}
        >
            {props.children}
        </GMap>
    ));

class GoogleMap extends Component {
    constructor(props) {
        super(props);

        this.state = {
            dragged: false,
        };

        this.dragged = this.dragged.bind(this);
        this.onMapLoad = this.onMapLoad.bind(this);
        this.resize = this.resize.bind(this);
    }

    dragged() {
        this.setState({ dragged: true });
    }

    onMapLoad(map) {
        if (!map) return;

        this._map = map;
        this._mapContext = this._map.context.__SECRET_MAP_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;

        this._mapContext.addListener('drag', this.dragged);
    }

    resize() {
        window.google.maps.event.trigger(this._mapContext, 'resize');

        if (!this.state.dragged)
            this._mapContext.setCenter(this.props.defaultCenter);
    }

    render() {
        return (
            <AsyncMap
                googleMapURL={`https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key=${apiKey}`}
                loadingElement={<div>{'loading...'}</div>}
                onMapLoad={this.onMapLoad}
                {...this.props}
            />
        );
    }
}

GoogleMap.propTypes = exact({
    children: propTypes.any,
    containerElement: propTypes.object,
    defaultCenter: propTypes.object.isRequired,
    defaultZoom: propTypes.number,
    mapElement: propTypes.object,
    onClick: propTypes.func,
});

GoogleMap.defaultProps = {
    defaultCenter:{ lat: -25.363882, lng: 131.044922 },
    containerElement: (<div style={{ height: '500px', width: '100%' }} />),
    mapElement: (<div style={{ height: '500px', width: '100%' }} />),
    defaultZoom: 5,
    onClick: _.noop,
};

export default GoogleMap;