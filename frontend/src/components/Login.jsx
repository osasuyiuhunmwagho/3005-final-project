import React, { useState } from 'react'
import { memberAPI, adminAPI, trainerAPI } from '../services/api'

function Login({ onLogin }) {
  const [selectedRole, setSelectedRole] = useState(null)
  const [isRegistering, setIsRegistering] = useState(false)
  const [userId, setUserId] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  // Registration form state - different forms for each role
  const [memberForm, setMemberForm] = useState({
    name: '',
    email: '',
    date_of_birth: '',
    gender: '',
    phone: ''
  })

  const [trainerForm, setTrainerForm] = useState({
    name: '',
    email: '',
    specialization: '',
    phone: ''
  })

  const [adminForm, setAdminForm] = useState({
    name: '',
    email: '',
    role: ''
  })

  const handleRoleSelect = (role) => {
    setSelectedRole(role)
    setIsRegistering(false)
    setError('')
    setSuccess('')
    // Auto-show registration for all roles
    setIsRegistering(true)
  }

  const handleRegister = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setSuccess('')

    try {
      let response
      let idField
      let roleName

      switch (selectedRole) {
        case 'member':
          if (!memberForm.name || !memberForm.email) {
            setError('Name and email are required')
            setLoading(false)
            return
          }
          response = await memberAPI.create(memberForm)
          idField = 'member_id'
          roleName = 'Member'
          break
        case 'trainer':
          if (!trainerForm.name || !trainerForm.email) {
            setError('Name and email are required')
            setLoading(false)
            return
          }
          response = await trainerAPI.create(trainerForm)
          idField = 'trainer_id'
          roleName = 'Trainer'
          break
        case 'admin':
          if (!adminForm.name || !adminForm.email) {
            setError('Name and email are required')
            setLoading(false)
            return
          }
          response = await adminAPI.create(adminForm)
          idField = 'admin_id'
          roleName = 'Admin'
          break
        default:
          throw new Error('Invalid role')
      }

      if (response.data && response.data[idField]) {
        setSuccess(`${roleName} created successfully! Your ID is ${response.data[idField]}`)
        // Auto-login after registration
        setTimeout(() => {
          onLogin(selectedRole, response.data[idField])
        }, 1500)
      }
    } catch (err) {
      if (err.response?.status === 400) {
        setError(err.response.data.detail || 'Registration failed. Email may already exist.')
      } else {
        setError('Failed to register. Please check your backend is running.')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleLogin = async () => {
    if (!selectedRole || !userId) {
      setError('Please select a role and enter an ID')
      return
    }

    setLoading(true)
    setError('')
    setSuccess('')

    try {
      let response
      const id = parseInt(userId)

      switch (selectedRole) {
        case 'member':
          response = await memberAPI.getById(id)
          break
        case 'admin':
          response = await adminAPI.getById(id)
          break
        case 'trainer':
          response = await trainerAPI.getById(id)
          break
        default:
          throw new Error('Invalid role')
      }

      if (response.data) {
        onLogin(selectedRole, id)
      }
    } catch (err) {
      if (err.response?.status === 404) {
        setError(`${selectedRole.charAt(0).toUpperCase() + selectedRole.slice(1)} with ID ${userId} not found. Please create one first or use an existing ID.`)
      } else {
        setError('Failed to login. Please check your backend is running.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Fitness Center Management</h2>
        <p style={{ textAlign: 'center', color: '#666', marginBottom: '30px' }}>
          Select your role and enter your ID to continue
        </p>

        <div className="role-selector">
          <div
            className={`role-button ${selectedRole === 'member' ? 'selected' : ''}`}
            onClick={() => handleRoleSelect('member')}
          >
            <h3>Member</h3>
            <p>View classes, track health</p>
          </div>
          <div
            className={`role-button ${selectedRole === 'admin' ? 'selected' : ''}`}
            onClick={() => handleRoleSelect('admin')}
          >
            <h3>Admin</h3>
            <p>Manage system</p>
          </div>
          <div
            className={`role-button ${selectedRole === 'trainer' ? 'selected' : ''}`}
            onClick={() => handleRoleSelect('trainer')}
          >
            <h3>Trainer</h3>
            <p>Set availability</p>
          </div>
        </div>

        {selectedRole && isRegistering ? (
          <form onSubmit={handleRegister}>
            <h3 style={{ color: '#008080', marginBottom: '15px' }}>
              Register as {selectedRole.charAt(0).toUpperCase() + selectedRole.slice(1)}
            </h3>

            {/* Member Registration Form */}
            {selectedRole === 'member' && (
              <>
                <div className="form-group">
                  <label>Name *</label>
                  <input
                    type="text"
                    value={memberForm.name}
                    onChange={(e) => setMemberForm({ ...memberForm, name: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Email *</label>
                  <input
                    type="email"
                    value={memberForm.email}
                    onChange={(e) => setMemberForm({ ...memberForm, email: e.target.value })}
                    required
                  />
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '10px' }}>
                  <div className="form-group">
                    <label>Date of Birth</label>
                    <input
                      type="date"
                      value={memberForm.date_of_birth}
                      onChange={(e) => setMemberForm({ ...memberForm, date_of_birth: e.target.value })}
                    />
                  </div>
                  <div className="form-group">
                    <label>Gender</label>
                    <select
                      value={memberForm.gender}
                      onChange={(e) => setMemberForm({ ...memberForm, gender: e.target.value })}
                    >
                      <option value="">Select...</option>
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                </div>
                <div className="form-group">
                  <label>Phone</label>
                  <input
                    type="tel"
                    value={memberForm.phone}
                    onChange={(e) => setMemberForm({ ...memberForm, phone: e.target.value })}
                    placeholder="(optional)"
                  />
                </div>
              </>
            )}

            {/* Trainer Registration Form */}
            {selectedRole === 'trainer' && (
              <>
                <div className="form-group">
                  <label>Name *</label>
                  <input
                    type="text"
                    value={trainerForm.name}
                    onChange={(e) => setTrainerForm({ ...trainerForm, name: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Email *</label>
                  <input
                    type="email"
                    value={trainerForm.email}
                    onChange={(e) => setTrainerForm({ ...trainerForm, email: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Specialization</label>
                  <input
                    type="text"
                    value={trainerForm.specialization}
                    onChange={(e) => setTrainerForm({ ...trainerForm, specialization: e.target.value })}
                    placeholder="e.g., Yoga, Strength Training (optional)"
                  />
                </div>
                <div className="form-group">
                  <label>Phone</label>
                  <input
                    type="tel"
                    value={trainerForm.phone}
                    onChange={(e) => setTrainerForm({ ...trainerForm, phone: e.target.value })}
                    placeholder="(optional)"
                  />
                </div>
              </>
            )}

            {/* Admin Registration Form */}
            {selectedRole === 'admin' && (
              <>
                <div className="form-group">
                  <label>Name *</label>
                  <input
                    type="text"
                    value={adminForm.name}
                    onChange={(e) => setAdminForm({ ...adminForm, name: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Email *</label>
                  <input
                    type="email"
                    value={adminForm.email}
                    onChange={(e) => setAdminForm({ ...adminForm, email: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Role</label>
                  <input
                    type="text"
                    value={adminForm.role}
                    onChange={(e) => setAdminForm({ ...adminForm, role: e.target.value })}
                    placeholder="e.g., Manager, Staff (optional)"
                  />
                </div>
              </>
            )}

            {error && <div className="alert alert-error">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}
            <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
                style={{ flex: 1 }}
              >
                {loading ? 'Registering...' : 'Register'}
              </button>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => setIsRegistering(false)}
                disabled={loading}
              >
                Login Instead
              </button>
            </div>
          </form>
        ) : selectedRole && (
          <>
            <div className="form-group">
              <label>
                {selectedRole.charAt(0).toUpperCase() + selectedRole.slice(1)} ID:
              </label>
              <input
                type="number"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                placeholder={`Enter ${selectedRole} ID`}
                onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
              />
            </div>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => setIsRegistering(true)}
              style={{ width: '100%', marginBottom: '10px' }}
            >
              New {selectedRole.charAt(0).toUpperCase() + selectedRole.slice(1)}? Register Here
            </button>
            {error && <div className="alert alert-error">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}
            <button
              className="btn btn-primary"
              onClick={handleLogin}
              disabled={!selectedRole || !userId || loading}
              style={{ width: '100%', marginTop: '10px' }}
            >
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </>
        )}

        {selectedRole && !isRegistering && (
          <p style={{ textAlign: 'center', marginTop: '20px', fontSize: '12px', color: '#666' }}>
            New {selectedRole}s can register above. Existing {selectedRole}s can login with their ID.
          </p>
        )}
      </div>
    </div>
  )
}

export default Login

