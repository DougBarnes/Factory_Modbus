
"""
Factory Job Queue class
Depends on factory_inventory
"""

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # sets default logging level for all modules

class JobQueue():
    """
    Factory Job Queue class
    Depends on factory_inventory
    """
    def __init__(self):
        """Initialize"""
        self.data = []
        logger.debug("Job Queue initialized")


    def add_job(self, order_data):
        """Add job to Queue"""
        logger.debug("Adding order to queue: %s", order_data)
        self.data.append(order_data)


    def cancel_job_order(self, order_id=None):
        """
        Search all jobs and delete each job with matching order ID
        """
        logger.info("Scanning queue to delete order_id: %s", order_id)
        items_deleted = 0
        return_msg = []
        for item in enumerate(self.data):
            logger.debug("Scanning Item: {}\tdata: {}".format(item[0], item[1]))
            if item[1]['order_id'] == order_id:
                return_msg.append("Deleting Job #: {} from order {}".format(item[1]['job_id'], item[1]['order_id']))
                logger.info(return_msg)
                del self.data[item[0]]
                items_deleted += 1

        if items_deleted > 0:
            logger.info("Deleted {} jobs".format(items_deleted))
        else:
            logger.warning("Could not find any jobs matching order_id {}".format(order_id))
            return_msg = "Could not find any jobs matching order_id {}".format(order_id)
            return (1, return_msg)

        return  (0, return_msg)


    def cancel_job_id(self, job_id=None):
        """Search queue for job id and delete"""
        logger.info("Scanning queue to delete job_id: {}".format(job_id))
        return_msg = ""
        for item in enumerate(self.data):
            logger.debug("Scanning Item: {}\tdata: {}".format(item[0], item[1]))
            if item[1]['job_id'] == job_id:
                return_msg = "Deleting Job #: {} from order {}".format(item[1]['job_id'], item[1]['order_id'])
                logger.info(return_msg)
                del self.data[item[0]]
                return (0, return_msg)

        logger.warning("Could not find any jobs matching job_id %d found", job_id)

        return (1, "Could not find any jobs matching job_id %d found", job_id)


    # Returns number of jobs
    def has_jobs(self):
        """Return queue length"""
        return len(self.data)


    def print_jobs(self):
        """Print out job data"""
        if len(self.data) == 0:
            logger.info("No jobs available to print")
        else:
            for item in self.data:
                logger.info("Item: %s", item)


    def next_job(self):
        """
        Pops next job if available & return job info
        """
        if len(self.data) == 0:
            logger.warning("No items in queue!")
            return 0

        return self.data.pop()

    # pop next job with available inventory
    def next_available_job(self, inventory):
        '''
        Look at first job
        Get it's color
        Try to pop an inventory slot with color
            if yes, pop job
            if no, pass to next job
        '''
        for job in enumerate(self.data):
            logger.debug("Looking at possible next job {}".format(job))
            job_color = job[1]['color']
            logger.debug("> job color: {}".format(job_color))

            # Check inventory for color
            slot = inventory.pop_color(job_color)
            if slot is False: # no color found in inventory
                continue # look at next job
            else:
                logger.info("Found available job {} for color {} in slot {}".format(job[1], job_color, slot))
                del self.data[job[0]]   # Delete job in queue
                return (job[1], slot)           # Pass back job data

        logger.info("Could not find a job with available inventory")
        return False