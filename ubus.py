from cffi import FFI
ffi = FFI()

# uBus
ffi.cdef("""
	void free(void*);

	typedef void (*uloop_fd_handler)(struct uloop_fd *u, unsigned int events);

	struct uloop_fd
	{
		uloop_fd_handler cb;
		int fd;
		bool eof;
		bool error;
		bool registered;
		uint8_t flags;
	};
	
	int uloop_init(void);
	
	int uloop_fd_add(struct uloop_fd *sock, unsigned int flags);

	enum blobmsg_type {
		BLOBMSG_TYPE_UNSPEC,
		BLOBMSG_TYPE_ARRAY,
		BLOBMSG_TYPE_TABLE,
		BLOBMSG_TYPE_STRING,
		BLOBMSG_TYPE_INT64,
		BLOBMSG_TYPE_INT32,
		BLOBMSG_TYPE_INT16,
		BLOBMSG_TYPE_INT8,
		__BLOBMSG_TYPE_LAST,
	};

	struct blobmsg_policy {
		const char *name;
		enum blobmsg_type type;
	};

	#pragma pack(1)
	struct blob_attr {
		uint32_t id_len;
		char data[];
	};
	#pragma pack(4)
	
	struct blob_buf {
		struct blob_attr *head;
		bool (*grow)(struct blob_buf *buf, int minlen);
		int buflen;
		void *buf;
	};
	
	int blob_buf_init(struct blob_buf *buf, int id);
	
	bool blobmsg_add_json_from_string(struct blob_buf *b, const char *str);
	bool blobmsg_add_json_from_file(struct blob_buf *b, const char *file);

	typedef const char *(*blobmsg_json_format_t)(void *priv, struct blob_attr *attr);

	char *blobmsg_format_json_with_cb(struct blob_attr *attr, bool list,
					  blobmsg_json_format_t cb, void *priv,
					  int indent);



	struct list_head {
		struct list_head *next;
		struct list_head *prev;
	};
	
	typedef int (*avl_tree_comp) (const void *k1, const void *k2, void *ptr);

	/**
	 * This element is a member of a avl-tree. It must be contained in all
	 * larger structs that should be put into a tree.
	 */
	struct avl_node {
		/**
		* Linked list node for supporting easy iteration and multiple
		* elments with the same key.
		*
		* this must be the first element of an avl_node to
		* make casting for lists easier
		*/
		struct list_head list;

		/**
		* Pointer to parent node in tree, NULL if root node
		*/
		struct avl_node *parent;

		/**
		* Pointer to left child
		*/
		struct avl_node *left;

		/**
		* Pointer to right child
		*/
		struct avl_node *right;

		/**
		* pointer to key of node
		*/
		const void *key;

		/**
		* balance state of AVL tree (0,-1,+1)
		*/
		signed char balance;

		/**
		* true if first of a series of nodes with same key
		*/
		bool leader;
	};

	struct avl_tree {
		/**
		* Head of linked list node for supporting easy iteration
		* and multiple elments with the same key.
		*/
		struct list_head list_head;

		/**
		* pointer to the root node of the avl tree, NULL if tree is empty
		*/
		struct avl_node *root;

		/**
		* number of nodes in the avl tree
		*/
		unsigned int count;

		/**
		* true if multiple nodes with the same key are
		* allowed in the tree, false otherwise
		*/
		bool allow_dups;

		/**
		* pointer to the tree comparator
		*
		* First two parameters are keys to compare,
		* third parameter is a copy of cmp_ptr
		*/
		avl_tree_comp comp;

		/**
		* custom pointer delivered to the tree comparator
		*/
		void *cmp_ptr;
	};

	struct ubus_msghdr {
		uint8_t version;
		uint8_t type;
		uint16_t seq;
		uint32_t peer;
	} __packetdata;

	enum ubus_msg_type {
		/* initial server message */
		UBUS_MSG_HELLO,

		/* generic command response */
		UBUS_MSG_STATUS,

		/* data message response */
		UBUS_MSG_DATA,

		/* ping request */
		UBUS_MSG_PING,

		/* look up one or more objects */
		UBUS_MSG_LOOKUP,

		/* invoke a method on a single object */
		UBUS_MSG_INVOKE,

		UBUS_MSG_ADD_OBJECT,
		UBUS_MSG_REMOVE_OBJECT,

		/*
		 * subscribe/unsubscribe to object notifications
		 * The unsubscribe message is sent from ubusd when
		 * the object disappears
		 */
		UBUS_MSG_SUBSCRIBE,
		UBUS_MSG_UNSUBSCRIBE,

		/*
		 * send a notification to all subscribers of an object.
		 * when sent from the server, it indicates a subscription
		 * status change
		 */
		UBUS_MSG_NOTIFY,

		/* must be last */
		__UBUS_MSG_LAST,
	};

	enum ubus_msg_attr {
		UBUS_ATTR_UNSPEC,

		UBUS_ATTR_STATUS,

		UBUS_ATTR_OBJPATH,
		UBUS_ATTR_OBJID,
		UBUS_ATTR_METHOD,

		UBUS_ATTR_OBJTYPE,
		UBUS_ATTR_SIGNATURE,

		UBUS_ATTR_DATA,
		UBUS_ATTR_TARGET,

		UBUS_ATTR_ACTIVE,
		UBUS_ATTR_NO_REPLY,

		UBUS_ATTR_SUBSCRIBERS,

		/* must be last */
		UBUS_ATTR_MAX,
	};

	enum ubus_msg_status {
		UBUS_STATUS_OK,
		UBUS_STATUS_INVALID_COMMAND,
		UBUS_STATUS_INVALID_ARGUMENT,
		UBUS_STATUS_METHOD_NOT_FOUND,
		UBUS_STATUS_NOT_FOUND,
		UBUS_STATUS_NO_DATA,
		UBUS_STATUS_PERMISSION_DENIED,
		UBUS_STATUS_TIMEOUT,
		UBUS_STATUS_NOT_SUPPORTED,
		UBUS_STATUS_UNKNOWN_ERROR,
		UBUS_STATUS_CONNECTION_FAILED,
		__UBUS_STATUS_LAST
	};

	struct ubus_context;
	struct ubus_msg_src;
	struct ubus_object;
	struct ubus_request;
	struct ubus_request_data;
	struct ubus_object_data;
	struct ubus_event_handler;
	struct ubus_subscriber;
	struct ubus_notify_request;

	typedef void (*ubus_lookup_handler_t)(struct ubus_context *ctx,
						  struct ubus_object_data *obj,
						  void *priv);
	typedef int (*ubus_handler_t)(struct ubus_context *ctx, struct ubus_object *obj,
					  struct ubus_request_data *req,
					  const char *method, struct blob_attr *msg);
	typedef void (*ubus_state_handler_t)(struct ubus_context *ctx, struct ubus_object *obj);
	typedef void (*ubus_remove_handler_t)(struct ubus_context *ctx,
						  struct ubus_subscriber *obj, uint32_t id);
	typedef void (*ubus_event_handler_t)(struct ubus_context *ctx, struct ubus_event_handler *ev,
						 const char *type, struct blob_attr *msg);
	typedef void (*ubus_data_handler_t)(struct ubus_request *req,
						int type, struct blob_attr *msg);
	typedef void (*ubus_fd_handler_t)(struct ubus_request *req, int fd);
	typedef void (*ubus_complete_handler_t)(struct ubus_request *req, int ret);
	typedef void (*ubus_notify_complete_handler_t)(struct ubus_notify_request *req,
							   int idx, int ret);
	typedef void (*ubus_connect_handler_t)(struct ubus_context *ctx);

	struct ubus_method {
		const char *name;
		ubus_handler_t handler;

		const struct blobmsg_policy *policy;
		int n_policy;
	};

	struct ubus_object_type {
		const char *name;
		uint32_t id;

		const struct ubus_method *methods;
		int n_methods;
	};

	struct ubus_object {
		struct avl_node avl;

		const char *name;
		uint32_t id;

		const char *path;
		struct ubus_object_type *type;

		ubus_state_handler_t subscribe_cb;
		bool has_subscribers;

		const struct ubus_method *methods;
		int n_methods;
	};

	struct ubus_subscriber {
		struct ubus_object obj;

		ubus_handler_t cb;
		ubus_remove_handler_t remove_cb;
	};

	struct ubus_event_handler {
		struct ubus_object obj;

		ubus_event_handler_t cb;
	};

	struct ubus_context {
		struct list_head requests;
		struct avl_tree objects;
		struct list_head pending;

		struct uloop_fd sock;

		uint32_t local_id;
		uint16_t request_seq;
		int stack_depth;

		void (*connection_lost)(struct ubus_context *ctx);

		struct {
			struct ubus_msghdr hdr;
			char data[65536];
		} msgbuf;
	};

	struct ubus_object_data {
		uint32_t id;
		uint32_t type_id;
		const char *path;
		struct blob_attr *signature;
	};

	struct ubus_request_data {
		uint32_t object;
		uint32_t peer;
		uint16_t seq;

		/* internal use */
		bool deferred;
		int fd;
	};

	struct ubus_request {
		struct list_head list;

		struct list_head pending;
		int status_code;
		bool status_msg;
		bool blocked;
		bool cancelled;
		bool notify;

		uint32_t peer;
		uint16_t seq;

		ubus_data_handler_t raw_data_cb;
		ubus_data_handler_t data_cb;
		ubus_fd_handler_t fd_cb;
		ubus_complete_handler_t complete_cb;

		struct ubus_context *ctx;
		void *priv;
	};

	struct ubus_notify_request {
		struct ubus_request req;

		ubus_notify_complete_handler_t status_cb;
		ubus_notify_complete_handler_t complete_cb;

		uint32_t pending;
		uint32_t id[17];
	};

	struct ubus_auto_conn {
		struct ubus_context ctx;
		struct uloop_timeout timer;
		const char *path;
		ubus_connect_handler_t cb;
	};
	
	struct ubus_context *ubus_connect(const char *path);
	void ubus_auto_connect(struct ubus_auto_conn *conn);
	int ubus_reconnect(struct ubus_context *ctx, const char *path);
	void ubus_free(struct ubus_context *ctx);

	const char *ubus_strerror(int error);

	/* ----------- raw request handling ----------- */

	/* wait for a request to complete and return its status */
	int ubus_complete_request(struct ubus_context *ctx, struct ubus_request *req,
				  int timeout);

	/* complete a request asynchronously */
	void ubus_complete_request_async(struct ubus_context *ctx,
					 struct ubus_request *req);

	/* abort an asynchronous request */
	void ubus_abort_request(struct ubus_context *ctx, struct ubus_request *req);

	/* ----------- objects ----------- */

	int ubus_lookup(struct ubus_context *ctx, const char *path,
			ubus_lookup_handler_t cb, void *priv);

	int ubus_lookup_id(struct ubus_context *ctx, const char *path, uint32_t *id);

	/* make an object visible to remote connections */
	int ubus_add_object(struct ubus_context *ctx, struct ubus_object *obj);

	/* remove the object from the ubus connection */
	int ubus_remove_object(struct ubus_context *ctx, struct ubus_object *obj);

	/* add a subscriber notifications from another object */
	int ubus_register_subscriber(struct ubus_context *ctx, struct ubus_subscriber *obj);

	int ubus_subscribe(struct ubus_context *ctx, struct ubus_subscriber *obj, uint32_t id);
	int ubus_unsubscribe(struct ubus_context *ctx, struct ubus_subscriber *obj, uint32_t id);

	/* ----------- rpc ----------- */

	/* invoke a method on a specific object */
	int ubus_invoke(struct ubus_context *ctx, uint32_t obj, const char *method,
			struct blob_attr *msg, ubus_data_handler_t cb, void *priv,
			int timeout);

	/* asynchronous version of ubus_invoke() */
	int ubus_invoke_async(struct ubus_context *ctx, uint32_t obj, const char *method,
				  struct blob_attr *msg, struct ubus_request *req);

	/* send a reply to an incoming object method call */
	int ubus_send_reply(struct ubus_context *ctx, struct ubus_request_data *req,
				struct blob_attr *msg);

	void ubus_complete_deferred_request(struct ubus_context *ctx,
						struct ubus_request_data *req, int ret);

	/*
	 * send a notification to all subscribers of an object
	 * if timeout < 0, no reply is expected from subscribers
	 */
	int ubus_notify(struct ubus_context *ctx, struct ubus_object *obj,
			const char *type, struct blob_attr *msg, int timeout);

	int ubus_notify_async(struct ubus_context *ctx, struct ubus_object *obj,
				  const char *type, struct blob_attr *msg,
				  struct ubus_notify_request *req);


	/* ----------- events ----------- */

	int ubus_send_event(struct ubus_context *ctx, const char *id,
				struct blob_attr *data);

	int ubus_register_event_handler(struct ubus_context *ctx,
					struct ubus_event_handler *ev,
					const char *pattern);

""")

# ubus libarary access variable
ubus = ffi.dlopen('libubus.so')

# json wrapper for ubus messages access variable
json = ffi.dlopen('libblobmsg_json.so')
# ANSI C access variable
C = ffi.dlopen(None)


###################################################################################
###################################################################################
###################################################################################
###################################################################################


################################################
#
# Global variables
#

# global variable of ubus context (should be initialized before use)
ctx = ffi.new("struct ubus_context *")
# global variable for last JSON response
json_resp = []

# create server ID
id = ffi.new("unsigned int[1]", [0])
# create BLOB buffer
b = ffi.new("struct blob_buf[1]")
	
#######################################################
#
# Callback functions (will be called from C library)
#

# parser callback for uBus response (simple format)
@ffi.callback("void(struct ubus_request*, int, struct blob_attr*)")
def simple_parse_callback(req, type, msg):
	# use gloabal string variable
	global json_resp

	c_json_resp = ffi.new("char*")

	# format blob as JSON
	c_json_resp = json.blobmsg_format_json_with_cb(msg, 1, ffi.NULL, ffi.NULL, -1)
	json_resp = ffi.string(c_json_resp)

	C.free(c_json_resp)

#	print json_resp

	return None
	
# parser callback for uBus response (human-friendly format)
@ffi.callback("void(struct ubus_request*, int, struct blob_attr*)")
def human_friendly_parse_callback(req, type, msg):
	# use gloabal string variable
	global json_resp
	global c_json_resp

	# format blob as JSON
	c_json_resp = json.blobmsg_format_json_with_cb(msg, 1, ffi.NULL, ffi.NULL, 0)
	json_resp = ffi.string(c_json_resp)

#	print json_resp

	return None
	
################################################
#
# Application APIs
#

def InitializeUBusClient( ubus_obj ):
	ubus_socket = ffi.new("char *")
	ubus_socket = ffi.NULL
	
	global ctx
	ctx = ffi.NULL

	# Connect socket and get context pointer
	ctx = ubus.ubus_connect(ubus_socket)
	
	# Check that context allocation succeeded
	if ctx == ffi.NULL:
		print "Could not connect to uBus"
		return None
		
	res = ubus.ubus_lookup_id(ctx, ubus_obj, ffi.cast("uint32_t*", id))
	if res != 0:
		print "Can't find server; err: ", ffi.string(ubus.ubus_strerror(res))
		return None

	return None

def SendJsonRequest( opr, json_req, output_fmt ):
	# use initialized before UBUS context
	global ctx
	global json_resp
	global id
	global b

	# initialize BLOB buffer
	ret = ubus.blob_buf_init(b, 0)
	if ret != 0:
		print "Can't create BLOB: ", ret, "\n"
		return ""

	# add JSON-formated request
	if json_req != "":
		ret = json.blobmsg_add_json_from_string(b, json_req)
		if ret != 1:
			print "Can't create BLOB from JSON ", json_req, "\n"
			return ""
	
	# send request to UBUS and parse it
	if output_fmt == 0:
		# invoke human-friendly parser
		ret = ubus.ubus_invoke(ctx, id[0], opr, b[0].head, human_friendly_parse_callback, ffi.NULL, 3000)
	else:
		# invoke simple parser
		ret = ubus.ubus_invoke(ctx, id[0], opr, b[0].head, simple_parse_callback, ffi.NULL, 3000)
	if ret != 0:
		return ""

	return json_resp

def DestroyUBusClient():
	# use initialized before UBUS context
	global ctx

	# release uBus context after use
	return ubus.ubus_free(ctx)
