hardware_fragment = """
fragment HardwareFragment on Hardware {
  id
  pk
  name
  slug
  createdAt
  updatedAt
  isAvailable
  isOnline
  isQuarantined
  isHealthy
  systemInfo
  hostname
  sshUsername
  capabilities {
    id
    pk
  }
  organization {
    id
    pk
    name
    slug
  }
  activeReservation {
    id
    pk
    status
    createdBy {
      username
    }
  }
}
"""
