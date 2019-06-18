import React, { Component } from 'react';

class Dryer extends Component {
  constructor() {
    super();
    this.state = {
      'applianceStandard': '',
      'brand': '',
      'Capacity': '',
      'Combination': '',
      'Control': '',
      'Country': '',
      'Depth': '',
      'Height': '',
      'Current_Comparitive_Energy_Consumption': '',
      'Program_Name': '',
      'Program_Time': '',
      'Type': '',
      'Width': '',
    }
    this.handleChange = this.handleChange.bind(this);
    this.submitForm = this.submitForm.bind(this);
  }
  handleChange(event) {
    event.preventDefault();
    this.setState({ [event.target.name] : event.target.value });
  }
  submitForm(e) {
    e.preventDefault();
    const data = [
    this.state.applianceStandard,
    this.state.brand,
    parseInt(this.state.Capacity),
    JSON.parse(this.state.Combination),
    this.state.Control,
    this.state.Country,
    parseInt(this.state.Depth),
    parseInt(this.state.Height),
    parseInt(this.state.Current_Comparitive_Energy_Consumption),
    this.state.Program_Name,
    parseInt(this.state.Program_Time),
    this.state.Type,
    parseInt(this.state.Width)
  ];
    // console.log(data);
    fetch('api/predict/dryer', {
      method: 'POST',
      mode: 'cors',
      cache: 'no-cache',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
      },
      redirect: 'follow',
      referrer: 'no-referrer',
      body: JSON.stringify({
        "specifications": data
      }),
    })
      .then(response => response.json())
      .then(res => {
        console.log(res);
        this.setState({ response: res })
      })
  }
  render() {
    return (
      <div>
        <div className="container-fluid mb-5 display-4">
          Dryer Details
        </div>
        <form className="container w-50">

          <div className="form-group">
            <label className="form-inline">Appliance Standard</label>
            <input
              type='text'
              className="form-control"
              placeholder='Appliance Standard'
              name="applianceStandard"
              value={this.state.applianceStandard}
              onChange={this.handleChange}
            />
          </div>

          <div className="form-group">
            <label className="form-inline">Brand</label>
            <input
              type='text'
              className="form-control"
              placeholder='Brand'
              name='brand'
              value={this.state.brand}
              onChange={this.handleChange}
            />
          </div>

          <div className="form-group">
            <label className="form-inline">Capacity</label>
            <input
              type='number'
              className="form-control"
              placeholder='Capacity'
              name='Capacity'
              value={this.state.Capacity}
              onChange={this.handleChange}
            />
          </div>

          <div className="form-group">
            <label className="form-inline">Combination</label>
            <select
              className="form-control"
              placeholder='Combination'
              name='Combination'
              value={this.state.Combination}
              onChange={this.handleChange}
            >
              <option value="true">True</option>
              <option value="false">False</option>
            </select>
          </div>

          <div className="form-group">
            <label className='form-inline'>Control</label>
            <input
              type='text'
              className="form-control"
              placeholder='Control'
              name='Control'
              value={this.state.Control}
              onChange={this.handleChange}
            />
          </div>

          <div className="form-group">
            <label className='form-inline'>Country</label>
            <input
              type='text'
              className="form-control"
              placeholder='Country'
              name="Country"
              value={this.state.Country}
              onChange={this.handleChange}
            />
          </div>

          <div className="form-group">
            <label className='form-inline'>Depth</label>
            <input
              type='number'
              className="form-control"
              placeholder='Depth'
              name="Depth"
              value={this.state.Depth}
              onChange={this.handleChange}
            />
          </div>

          <div className="form-group">
            <label className='form-inline'>Height</label>
            <input
              type='number'
              className="form-control"
              placeholder='Height'
              name="Height"
              value={this.state.Height}
              onChange={this.handleChange}
            />
          </div>

          <div className="form-group">
            <label className='form-inline'>Current Comparitive Energy Consumption</label>
            <input
              type='number'
              className="form-control"
              placeholder='Current_Comparitive_Energy_Consumption'
              name="Current_Comparitive_Energy_Consumption"
              value={this.state.Current_Comparitive_Energy_Consumption}
              onChange={this.handleChange}
            />
          </div>

          <div className="form-group">
            <label className='form-inline'>Program_Name</label>
            <input
              type='text'
              className="form-control"
              placeholder='Program_Name'
              name="Program_Name"
              value={this.state.Program_Name}
              onChange={this.handleChange}
            />
          </div>

          <div className="form-group">
            <label className='form-inline'>Program_Time</label>
            <input
              type='number'
              className="form-control"
              placeholder='Program_Time'
              name="Program_Time"
              value={this.state.Program_Time}
              onChange={this.handleChange}
            />
          </div>

          <div className="form-group">
            <label className='form-inline'>Type</label>
            <input
              type='text'
              className="form-control"
              placeholder='Type'
              name="Type"
              value={this.state.Type}
              onChange={this.handleChange}
            />
          </div>

          <div className="form-group">
            <label className='form-inline'>Width</label>
            <input
              type='number'
              className="form-control"
              placeholder='Width'
              name="Width"
              value={this.state.Width}
              onChange={this.handleChange}
            />
          </div>
          <button
            type='submit'
            className='form-group btn btn-lg btn-success'
            onClick={this.submitForm}
          >
            Submit
          </button>
        </form>
      </div>

    );
  }
}

export default Dryer;