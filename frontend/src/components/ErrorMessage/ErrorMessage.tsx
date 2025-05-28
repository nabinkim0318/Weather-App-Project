interface ErrorMessageProps {
  message: string;
}

const ErrorMessage = ({ message }: ErrorMessageProps) => {
  return (
    <div className="mt-4 p-3 bg-red-100 text-red-800 rounded-lg">
      <i className="fas fa-exclamation-circle mr-2"></i>
      {message}
    </div>
  );
};

export default ErrorMessage;
